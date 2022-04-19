import functools
import json, os
import operator
import time
from itertools import product
from multiprocessing import Pool
from pprint import pprint

import numpy as np
from multimethod import isa, overload
from pyspark.sql import DataFrame, Window
from pyspark.sql.functions import monotonically_increasing_id, asc, col, ntile

from pycats.structure.plant.spark import Plant

def flattenDict(l):
    def tupalize(k, vs):
        l = []
        if isinstance(vs, list):
            for v in vs:
                l.append((k, v))
        else:
            l.append((k, vs))
        return l

    flat_list = [tupalize(k, vs) for k, vs in l.items()]
    flat_dict = [dict(items) for items in product(*flat_list)]
    return flat_dict

def flatten(l):
    if isinstance(l, list):
        return functools.reduce(operator.iconcat, l, [])
    elif isinstance(l, dict):
        return flattenDict(l)

def split_by_row_index(df, num_partitions):
    # Let's assume you don't have a row_id column that has the row order
    t = df.withColumn('_row_id', monotonically_increasing_id())
    # Using ntile() because monotonically_increasing_id is discontinuous across partitions
    t = t.withColumn('_partition', ntile(num_partitions).over(Window.orderBy(t._row_id)))
    return [t.filter(t._partition == i + 1).drop('_row_id', '_partition') for i in range(num_partitions)]

def content_address_partition(
        content_address_dataset,
        input_data_json_df_uri: str,
        invoice_uri: str,
        part: int,
        part_df: DataFrame
):
    df_dir = input_data_json_df_uri.split('/')[-1]
    input_data_part_json_uri = input_data_json_df_uri.replace(df_dir, f'{df_dir}_{part}')
    # pprint(part)
    # pprint(input_data_json_df_uri)
    # pprint(input_data_json_df_uri.replace('df_json', f'df_json_{part}'))
    # while True:
    #     time.sleep(1)
    part_df.repartition(1).write.json(input_data_part_json_uri, mode='overwrite')
    cai_invoice_part_uri = invoice_uri.replace('/invoices/', f'/invoice_{part}/')

    (
        input_cad_invoice,
        invoice_cid,
        ip4_tcp_addresses
    ) = content_address_dataset(input_data_part_json_uri, cai_invoice_part_uri, part)
    return {
        'input_data_part_json_uri': input_data_part_json_uri,
        'input_cad_invoice': input_cad_invoice,
        'invoice_cid': invoice_cid,
        'ip4_tcp_addresses': ip4_tcp_addresses
    }


CATS_HOME = os.getenv('CATS_HOME')
class Processor(Plant):
    def __init__(self,
        plantSession,
        DRIVER_IPFS_DIR=f'{CATS_HOME}/cadStore'
    ):
        Plant.__init__(self, plantSession, DRIVER_IPFS_DIR)

        self.cai_invoice_cid = None
        self.cao_invoice_cid: str = None
        self.transform_func = None
        # self.transform_cid = None

        self.cai_bom_cid = None
        self.cai_bom = {}
        self.cao_bom = {}
        self.cat_log = {}

        self.ipfs_id = None
        self.daemon_pid = None
        self.daemon_proc = None
        self.ip4_tcp_addresses = None

    @overload
    def content_address_dataset(self, s3_bucket, s3_prefix, cai_invoice_uri, part=None):
        s3_input_keys = self.get_s3_keys(s3_bucket, s3_prefix)
        return self.create_invoice(s3_input_keys, cai_invoice_uri, part)

    @overload
    def content_address_dataset(self, s3_dataset_uri, cai_invoice_uri, part=None):
        dataset_s3_bucket, dataset_s3_prefix = self.get_s3_bucket_prefix_pair(s3_dataset_uri)
        return self.content_address_dataset(dataset_s3_bucket, dataset_s3_prefix, cai_invoice_uri, part)

    def content_address_input(
            self,
            input_data_uri,
            invoice_uri,
            output_data_uri,
            bom_write_path_uri,
            local_bom_write_path='/tmp/bom.json',
            transformer_uri=None
    ):
        input_data_uri = input_data_uri.replace('s3://', 's3a://')
        invoice_uri = invoice_uri.replace('s3://', 's3a://')
        output_data_uri = output_data_uri.replace('s3://', 's3a://')
        bom_write_path_uri = bom_write_path_uri.replace('s3a://', 's3://')
        transformer_uri = transformer_uri.replace('s3://', 's3a://')

        self.cai_bom['transformer_uri'] = transformer_uri
        self.cai_bom['cai_invoice_uri'] = self.catContext['cai_invoice_uri'] = invoice_uri
        self.cai_bom['cai_data_uri'] = output_data_uri
        self.cai_bom['bom_uri'] = bom_write_path_uri
        self.cai_bom['action'] = ''
        self.cai_bom['input_bom_cid'] = ''
        self.cai_bom, self.cat_log['transformer_addresses'] = self.content_address_transform(self.cai_bom) #ToDo: make generic for plant

        input_data_uri_split = input_data_uri.rsplit('/', 1)
        input_data_dir = input_data_uri_split[0] + '/'
        input_data_df_name = input_data_uri_split[1].split('.')[0]
        input_data_json_df_name = input_data_df_name + '_json'
        input_data_json_df_uri = f'{input_data_dir}{input_data_json_df_name}'
        input_data_df = self.spark.read.parquet(input_data_uri)
        # .drop(col("cat_idx")) \
        input_data_df \
            .withColumn("cat_idx", monotonically_increasing_id()) \
            .sort(asc("cat_idx")) \
            .repartition(1).write.json(input_data_json_df_uri, mode='overwrite')
        input_data_json_df = self.spark.read.json(input_data_json_df_uri)

        # copy_input_data_json_df = input_data_json_df
        input_data_s3_bucket, input_data_s3_prefix = self.get_s3_bucket_prefix_pair(input_data_uri)
        s3_input_keys = self.get_s3_keys(input_data_s3_bucket, input_data_s3_prefix)
        # n_input_splits = len(s3_input_keys)
        n_input_splits = 1
        # each_len = input_data_df.count() // n_input_splits



        # p = Pool(n_input_splits)
        # content_addressed_parts = p.map(
        #     content_address_partition,
        #     enumerate(split_by_row_index(input_data_json_df, n_input_splits))
        # )

        content_addressed_parts = [
            content_address_partition(
                self.content_address_dataset,
                input_data_json_df_uri,
                self.catContext['cai_invoice_uri'],
                part,
                part_df
            )
            for part, part_df in enumerate(split_by_row_index(input_data_json_df, n_input_splits))
        ]
        input_cad_invoice_dfs = [self.spark.read.json(part['input_cad_invoice']) for part in content_addressed_parts]
        input_cad_invoices_df = functools.reduce(DataFrame.unionAll, input_cad_invoice_dfs)
        input_cad_invoices_df.write.json(self.catContext['cai_invoice_uri'], mode='overwrite')
        # input_cad_invoices_df.select('cid', 'file_key', 'filename').show(truncate=False)
        # cai_invoice_cids = list(set([part['invoice_cid'] for part in content_addressed_parts]))
        ip4_tcp_addresses_list = [part['ip4_tcp_addresses'] for part in content_addressed_parts]
        self.cat_log['addresses'] = list(set(flatten(ip4_tcp_addresses_list)))
        self.cai_bom['cai_part_cids'] = input_cad_invoices_df \
            .select('cid').sort('cid').distinct().rdd.map(lambda r: r[0]).collect()
        # pprint(cai_part_cids)
        # pprint(list(set(flatten(ip4_tcp_addresses_list))))
        # while True:
        #     time.sleep(1)

        # (
        #     input_cad_invoice,
        #     self.cai_bom['invoice_cid'],
        #     ip4_tcp_addresses
        # ) = self.content_address_dataset(input_data_json_df_uri, self.catContext['cai_invoice_uri'])
        # # ) = self.content_address_dataset(input_data_uri, self.catContext['cai_invoice_uri'])
        # ip4_tcp_addresses = list(set(flatten(ip4_tcp_addresses_list)))

        # # ic0df = input_cad_invoice.toDF()
        # ic1df = input_cad_invoices_df
        # # ic0 = ic0df.select('cid').sort('cid').distinct().collect()
        # # ic = input_cad_invoice.toDF().show()
        # cai_part_cids = input_cad_invoices_df.select('cid').sort('cid').distinct().rdd.map(lambda r: r[0]).collect()
        # pprint(cai_part_cids)
        #
        # # print()
        # # pprint(cai_part_cids)
        # print()
        # pprint(self.cat_log['addresses'])
        # # print()
        # # pprint(ic0)
        # print()
        # pprint(self.cai_bom['cai_part_cids'])
        # print()
        # # ic0df.show(truncate=False)
        # ic1df.show(truncate=False)
        # while True:
        #     time.sleep(1)

        # alt
        # self.cai_bom['addresses'] = np.unique(
        #     np.array(ip4_tcp_addresses)
        # ).tolist()

        # self.cat_log['addresses'] = np.unique(np.array(ip4_tcp_addresses)).tolist()
        self.cai_bom = self.save_bom(self.cai_bom, 'cai')
        # self.cai_invoice_cid = self.cai_bom['invoice_cid']
        self.cai_part_cids = input_cad_invoices_df.select('cid').sort('cid').distinct().rdd.map(lambda r: r[0]).collect()
        self.cai_bom['cai_part_cids'] = self.cai_part_cids
        cai_bom_df = self.create_bom_df(self.cai_bom)
        # cai_bom_df.write.json(self.cai_bom_uri, mode='overwrite')
        # return input_cad_invoice
        with open(local_bom_write_path, 'w') as fp:
            cai_bom_dict = self.bom_df_to_dict(cai_bom_df)
            json.dump(cai_bom_dict, fp)

        # self.boto3_cp(local_bom_write_path, bom_write_path_uri)
        self.aws_cli_cp(local_bom_write_path, bom_write_path_uri)

        bom_split = self.cai_bom['bom_uri'].rsplit('/', 1)
        bom_dir = bom_split[0] + '/'
        bom_name = bom_split[1].split('.')[0]
        log_name = bom_name + '_cat_log.json'
        local_log_write_path = f'/tmp/{log_name}'

        with open(local_log_write_path, 'w') as fp:
            cat_log_df = self.create_bom_df(self.cat_log)
            cat_log_dict = self.bom_df_to_dict(cat_log_df)
            json.dump(cat_log_dict, fp)

        log_write_path_uri = bom_dir + log_name
        self.aws_cli_cp(local_log_write_path, log_write_path_uri)

        # return cai_bom_dict, input_cad_invoice
        return cai_bom_dict, input_cad_invoices_df

    def content_address_output(self, cao_bom: isa(dict), local_bom_write_path: isa(str)):
        cai_data_uri = cao_bom['cai_data_uri']  # I
        cai_invoice_uri = cao_bom['cai_invoice_uri']  # O
        s3_bom_write_path = cao_bom['cad_bom_uri']  # O
        cao_bom['cao_data_uri'] = ''
        cao_bom['action'] = ''
        self.cao_bom, self.cat_log['transformer_addresses'] = self.content_address_transform(cao_bom) # ToDo: make generic for plant

        cai_data_uri_split = cai_data_uri.rsplit('/', 1)
        cai_data_dir = cai_data_uri_split[0] + '/'
        cai_data_df_name = cai_data_uri_split[1].split('.')[0]
        cai_data_json_df_name = cai_data_df_name + '_json'
        cai_data_json_df_uri = f'{cai_data_dir}{cai_data_json_df_name}'.replace('s3://', 's3a://')
        cai_data_df = self.spark.read.parquet(cai_data_uri)
        cai_data_df \
            .withColumn("cat_idx", monotonically_increasing_id()) \
            .sort(asc("cat_idx")) \
            .repartition(1).write.json(cai_data_json_df_uri, mode='overwrite')
        cai_data_json_df = self.spark.read.json(cai_data_json_df_uri)
        # self.spark.read.json(cai_data_json_df_uri).show()
        # exit()

        # # cai_data_json_df = self.spark.read.json(cai_data_json_df_uri)
        # # if 's3a://' in cai_data_uri:
        # #     cai_data_uri = cai_data_uri.replace("s3a:", "s3:")
        # (
        #     output_cad_invoice,
        #     self.cao_bom['invoice_cid'],
        #     ip4_tcp_addresses
        # ) = self.content_address_dataset(cai_data_json_df_uri, cai_invoice_uri)
        # # ) = self.content_address_dataset(cai_data_uri, cai_invoice_uri)
        # # alt
        # # self.cao_bom['addresses'] = np.unique(
        # #     np.array(ip4_tcp_addresses)
        # # ).tolist()

        cai_data_s3_bucket, cai_data_s3_prefix = self.get_s3_bucket_prefix_pair(cai_data_uri)
        s3_input_keys = self.get_s3_keys(cai_data_s3_bucket, cai_data_s3_prefix)
        # n_input_splits = len(s3_input_keys)
        n_input_splits = 1

        content_addressed_parts = [
            content_address_partition(
                self.content_address_dataset,
                cai_data_json_df_uri,
                self.catContext['cao_invoice_uri'],
                part,
                part_df
            )
            for part, part_df in enumerate(split_by_row_index(cai_data_json_df, n_input_splits))
        ]
        output_cad_invoice_dfs = [self.spark.read.json(part['input_cad_invoice']) for part in content_addressed_parts]
        output_cad_invoices_df = functools.reduce(DataFrame.unionAll, output_cad_invoice_dfs)
        output_cad_invoices_df.write.json(self.catContext['cao_invoice_uri'], mode='overwrite')
        ip4_tcp_addresses_list = [part['ip4_tcp_addresses'] for part in content_addressed_parts]
        self.cat_log['addresses'] = list(set(flatten(ip4_tcp_addresses_list)))
        self.cao_bom['cao_part_cids'] = output_cad_invoices_df \
            .select('cid').sort('cid').distinct().rdd.map(lambda r: r[0]).collect()

        # self.cat_log['addresses'] = np.unique(np.array(ip4_tcp_addresses)).tolist()
        self.cao_bom = self.save_bom(self.cao_bom, 'cao')
        cao_bom_df = self.create_bom_df(self.cao_bom)
        with open(local_bom_write_path, 'w') as fp:
            cao_bom_dict = self.bom_df_to_dict(cao_bom_df)
            json.dump(cao_bom_dict, fp)

        if 's3a://' in s3_bom_write_path:
            s3_bom_write_path = s3_bom_write_path.replace('s3a://', 's3://')
        # upload
        self.aws_cli_cp(local_bom_write_path, s3_bom_write_path)

        bom_split = local_bom_write_path.rsplit('/', 1)
        bom_dir = bom_split[0] + '/'
        bom_name = bom_split[1].split('.')[0]
        log_name = bom_name + '_cat_log.json'
        local_log_write_path = f'/tmp/{log_name}'

        with open(local_log_write_path, 'w') as fp:
            cat_log_df = self.create_bom_df(self.cat_log)
            cat_log_dict = self.bom_df_to_dict(cat_log_df)
            json.dump(cat_log_dict, fp)

        remote_bom_dir = s3_bom_write_path.rsplit('/', 1)[0] + '/'
        log_write_path_uri = remote_bom_dir + log_name
        self.aws_cli_cp(local_log_write_path, log_write_path_uri)

        # self.write_rdd_as_parquet(output_cad_invoices_df, self.cao_bom['cai_invoice_uri'])
        output_cad_invoices_df.write.parquet(self.cao_bom['cai_invoice_uri'].replace('s3://', 's3a://'), mode='overwrite')
        return cao_bom_dict, output_cad_invoices_df

    def set_cao_bom(self, ip4_tcp_addresses, cai_bom, output_bom_path):
        cao_bom = {}
        cao_bom['action'] = ''
        # cao_bom['addresses'] = ip4_tcp_addresses
        cao_bom['input_bom_cid'] = cai_bom['bom_cid']
        cao_bom['cai_invoice_uri'] = ''
        cao_bom['invoice_cid'] = ''  # rename to cai_invoice_cid
        cao_bom['transform_cid'] = ''
        cao_bom['transform_filename'] = ''
        cao_bom['transform_node_path'] = ''
        cao_bom['transform_uri'] = ''
        cao_bom['cad_bom_uri'] = output_bom_path
        return cao_bom

    @overload
    def transform(
            self,
            cai_bom: isa(dict),
            cao_bom: isa(dict)
    ):
        cai_bom['cai_data_uri'] = cai_bom['cai_data_uri'].replace('s3://', 's3a://')
        cai_bom['cao_data_uri'] = cai_bom['cao_data_uri'].replace('s3://', 's3a://')
        cai_bom['cai_invoice_uri'] = cai_bom['cai_invoice_uri'].replace('s3://', 's3a://')
        cai_bom['transformer_uri'] = cai_bom['transformer_uri'].replace('s3://', 's3a://')
        self.cai_invoice_uri = cai_bom['cai_invoice_uri']
        self.cao_data_uri = cai_bom['cao_data_uri']
        catContext = self.cad.execute(
            cai_invoice_uri=self.cai_invoice_uri,
            cao_data_uri=self.cao_data_uri,
            transform_func=self.transform_func
        )
        self.write_df_as_parquet(catContext['cai'], cao_bom['cai_data_uri'])
        return catContext, cai_bom, cao_bom

    @overload
    def transform(
            self,
            input_bom_path: isa(str),
            output_bom_path: isa(str),
            cat_log_path: isa(str),
            input_bom_update: isa(dict) = None,
            output_bom_update: isa(dict) = None
    ):
        self.cai_bom = self.get_input_bom_from_s3(input_bom_path)
        with open(cat_log_path) as cat_log_file:
            self.cat_log = json.load(cat_log_file)

        if input_bom_update is not None:
            self.cai_bom.update(input_bom_update)

        try:
            self.ipfs_swarm_connect(self.cai_bom['addresses'])
            self.transform_func = self.get_transform_func(self.cai_bom)
        except:
            self.transform_func = self.get_transform_func_s3(self.cai_bom)

        # self.ip4_tcp_addresses not assigned
        self.cao_bom = self.set_cao_bom(self.ip4_tcp_addresses, self.cai_bom, output_bom_path)
        if output_bom_update is not None:
            self.cao_bom.update(output_bom_update)
            self.catContext, self.cai_bom, self.cao_bom = self.transform(self.cai_bom, self.cao_bom)

            with open(self.cao_bom['transform_sourcefile'], 'rb') as cao_transform_file:
                transformer_bucket, transformer_key = self.get_s3_bucket_key_pair(self.cao_bom['transformer_uri'])
                self.s3_client.upload_fileobj(cao_transform_file, Bucket=transformer_bucket, Key=transformer_key)
            cao_transform_file.close()

            self.cao_bom, output_cad_invoice = self.content_address_output(
                cao_bom=self.cao_bom,
                local_bom_write_path='/tmp/bom.json'
            )

        else:
            self.catContext, self.cai_bom, self.cao_bom = self.transform(self.cai_bom, self.cao_bom)

        CAO_BOM_FILE_PATH = '/tmp/output_bom.json'
        with open(CAO_BOM_FILE_PATH, 'w') as f:
            json.dump(self.cao_bom, f)
            [_, self.cao_bom['cad_cid'], _] = self.ipfs_add(CAO_BOM_FILE_PATH)
            json.dump(self.cao_bom, f)
        f.close()
        with open(CAO_BOM_FILE_PATH, 'rb') as f:
            output_bom_bucket, output_bom_key = self.get_s3_bucket_key_pair(self.cao_bom['cad_bom_uri'])
            self.s3_client.upload_fileobj(f, Bucket=output_bom_bucket, Key=output_bom_key)
        f.close()

        return self