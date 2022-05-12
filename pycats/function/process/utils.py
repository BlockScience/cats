import os, subprocess, boto3, json, time
from operator import itemgetter

from pycats import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from pycats.function import WORK_DIR, INPUT, IPFS_DIR, OUTPUT, INVOICE_DIR, INPUT_DIR, TRANSFORM_DIR

s3_client = boto3.client(
    's3',
    region_name='us-east-2',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
s3_resource = boto3.resource(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
session = boto3.Session(
    region_name='us-east-2',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)


class s3Utils():
    def __init__(self):
        pass

    def get_s3_bucket_prefix_pair(self, path):
        scheme = f"{path.split(':')[0]}://"
        bucket = path.split(scheme)[1].split('/')[0]
        prefix = path.split(scheme)[1].split(bucket)[1][1:] + '/'
        return bucket, prefix

    def get_s3_bucket_key_pair(self, path):
        scheme = f"{path.split(':')[0]}://"
        bucket = path.split(scheme)[1].split('/')[0]
        key = path.split(scheme)[1].split(bucket)[1][1:]
        return bucket, key


# def content_address_tranformation(transform_uri):
def content_address_transformer(transform_uri):
    # 's3a://cats-public/cad-store/cad/transformation/transform.py'
    transform_bucket = transform_uri.split('s3a://')[-1].split('/')[0]
    transform_key = transform_uri.split('s3a://')[-1].split(transform_bucket)[-1][1:]
    transform_filename = transform_key.split('/')[-1]
    NODE_FILE_PATH = f"{TRANSFORM_DIR}/{transform_filename}"

    subprocess.check_call(f"mkdir -p {TRANSFORM_DIR}".split(' '))
    # if doesnt exist
    s3_client.download_file(Bucket=transform_bucket, Key=transform_key, Filename=NODE_FILE_PATH)
    ipfs_add = f'ipfs add {NODE_FILE_PATH}'.split(' ')
    [ipfs_action, cid, _file_name] = subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')

    ipfs_id = open(f'{IPFS_DIR}/ipfs_id.json')
    ipfs_addresses = json.load(ipfs_id)["Addresses"]
    ip4_tcp_addresses = [x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x)]
    transformer_addresses = ip4_tcp_addresses

    partial_bom = {
        'action': ipfs_action,
        'transform_cid': cid,
        'transform_uri': transform_uri,
        # 'transformer_addresses': ip4_tcp_addresses,
        'transform_filename': transform_filename,
        'transform_node_path': NODE_FILE_PATH
    }
    return partial_bom, transformer_addresses


def save_bom(bom_type: str = 'cao'):
    BOM_DIR = f"{WORK_DIR}/job/bom"
    BOM_FILE = f'{BOM_DIR}/{bom_type}_bom.json'
    def f(partial_bom):
        subprocess.check_call(f"mkdir -p {BOM_DIR}".split(' '))
        with open(BOM_FILE, 'w') as fp:
            json.dump(partial_bom, fp)
        ipfs_add = f'ipfs add {BOM_FILE}'.split(' ')
        [_, bom_cid, _file_name] = subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')
        partial_bom['bom_cid'] = bom_cid
        return partial_bom
    return f

def ensure_similarity(PARTPATH: str):
    if '.json' in PARTPATH:
        old_part_file = open(PARTPATH, "r+")
        os.remove(PARTPATH)
        part_json_lines = old_part_file.readlines()
        old_part_file.close()
        part_json_list = [json.loads(l[:len(l) - 1]) for l in part_json_lines]
        part_json_sorted_list = sorted(part_json_list, key=itemgetter('cat_idx'), reverse=False)

        def json_2_str(j):
            del j['cat_idx']
            return json.dumps(j)

        part_json_sorted_list = [json_2_str(j) for j in part_json_sorted_list]

        new_part_file = open(PARTPATH, "w")
        for j in part_json_sorted_list:
            new_part_file.write(f"{j}\n")
        new_part_file.close()
        return part_json_sorted_list

# Ingest
def cad_part_invoice(cad_part_id_dict, part=None):
    bucket = 'cats-public'
    file_path_key = cad_part_id_dict["FilePathKey"]
    file_name = file_path_key.split('/')[-1]

    NODE_FILE_PATH = f"{WORK_DIR}/job/{file_path_key}"
    ipfs_addresses = cad_part_id_dict["Addresses"]
    ip4_tcp_addresses = [x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x)]

    # INPUT = f"{WORK_DIR}/job/input/df"
    # OUTPUT = f"{WORK_DIR}/job/output/df"
    if part is not None:
        INPUT = f"{WORK_DIR}/job/input/df_json_{part}"
        OUTPUT = f"{WORK_DIR}/job/output/df_json_{part}"
    else:
        INPUT = f"{WORK_DIR}/job/input/df_json"
        OUTPUT = f"{WORK_DIR}/job/output/df_json"
    subprocess.check_call(f"mkdir -p {INPUT}".split(' '))
    subprocess.check_call(f"mkdir -p {OUTPUT}".split(' '))
    if '/job/input/df' in NODE_FILE_PATH:
        s3_client.download_file(Bucket=bucket, Key=file_path_key, Filename=NODE_FILE_PATH)  # delete after transfer
        part_json_sorted_list = ensure_similarity(NODE_FILE_PATH)
        if part is not None:
            # if '.json' in file_name:
            part_id = "-".join(file_name.split("-")[:2])
            cat_part_id = str(part).zfill(len(part_id.split('-')[1])) # part padding
            new_file_name = "part-" + cat_part_id + ".json"
            rename = f'mv {INPUT}/{file_name} {INPUT}/{new_file_name}'.split(' ')
            subprocess.check_output(rename)
            ipfs_add = f'ipfs add {INPUT}/{new_file_name}'.split(' ')
            file_name = new_file_name
        else:
            part_id = "-".join(file_name.split("-")[:2])
            new_file_name = part_id + ".json"
            rename = f'mv {INPUT}/{file_name} {INPUT}/{new_file_name}'.split(' ')
            subprocess.check_output(rename)
            ipfs_add = f'ipfs add {INPUT}/{file_name}'.split(' ')
    else:
        NODE_FILE_PATH = f"{OUTPUT}/{file_name}"
        s3_client.download_file(Bucket=bucket, Key=file_path_key, Filename=NODE_FILE_PATH)
        part_json_sorted_list = ensure_similarity(NODE_FILE_PATH)
        if part is not None:
            # if '.json' in file_name:
            part_id = "-".join(file_name.split("-")[:2])
            cat_part_id = str(part).zfill(len(part_id.split('-')[1])) # part padding
            new_file_name = "part-" + cat_part_id + ".json"
            rename = f'mv {OUTPUT}/{file_name} {OUTPUT}/{new_file_name}'.split(' ')
            subprocess.check_output(rename)
            ipfs_add = f'ipfs add {OUTPUT}/{new_file_name}'.split(' ')
            file_name = new_file_name
        else:
            part_id = "-".join(file_name.split("-")[:2])
            cat_part_id = str(part).zfill(len(part_id.split('-')[1]))  # part padding
            new_file_name = "part-" + cat_part_id + ".json"
            rename = f'mv {OUTPUT}/{file_name} {OUTPUT}/{new_file_name}'.split(' ')
            subprocess.check_output(rename)
            ipfs_add = f'ipfs add {OUTPUT}/{new_file_name}'.split(' ')
    [ipfs_action, cid, _file_name] = subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')

    return {
        'cid': cid,
        'addresses': ip4_tcp_addresses,
        'filename': file_name,
        'action': ipfs_action,
        'file_key': file_path_key,
        # 'records': part_json_sorted_list
    }

def ipfs_connect(cad_part_invoice):
    addresses = cad_part_invoice['addresses']
    try:
        for address in addresses:
            output = subprocess.check_output(f"ipfs swarm connect {address}".split(' ')) \
                .decode('ascii').replace('\n', '').split(' ')
            if output[2] == 'success':
                cad_part_invoice['connection'] = address
            else:
                cad_part_invoice['connection'] = None
            return cad_part_invoice
    except:
        cad_part_invoice['connection'] = None
        return cad_part_invoice


def s3_ingest(cad_part_invoice):
    cid = cad_part_invoice['cid']
    filename = cad_part_invoice['filename']
    bucket = 'cats-public'
    key = 'cad-store/cad/cai/parts'
    uri = f's3a://{bucket}/{key}'
    subprocess.check_call(f"mkdir -p {INPUT}".split(' '))

    os.chdir(INPUT)
    output = subprocess.check_output(f"ipfs get {cid}".split(' ')).decode('ascii').replace('\n', '')
    if output == f'Saving file(s) to {cid}':
        subprocess.check_call(f"mv {cid} {filename}".split(' '))
        try:
            in_file = INPUT + f"/{filename}"
            s3_client.upload_file(in_file, Bucket=bucket, Key=key+f'/{filename}')
            # file = open(in_file, "rb")
            # # file = open(filename, "rb")
            # s3_client.upload_fileobj(file, Bucket=bucket, Key=key)
            # file.close()
            # in_file = INPUT+f"/{filename}"
            # out_file = uri.replace('s3a://', 's3://')+f'/{filename}'
            # aws_cp = f"aws s3 cp {in_file} {out_file}"
            # subprocess.check_output(aws_cp, shell=True)
            cad_part_invoice['upload_path'] = uri
            return cad_part_invoice
        except Exception as e:
            cad_part_invoice['upload_path'] = str(e)
            return cad_part_invoice


def ipfs_caching(part=None):
    return lambda file_path_key: cad_part_invoice(link_ipfs_id(file_path_key), part)

def cluster_fs_ingest(cad_part_invoice):
    return s3_ingest(ipfs_connect(cad_part_invoice))


# CAD
def get_upload_path(cad_part_invoice):
    return str(cad_part_invoice['upload_path'])


# CAT
def link_ipfs_id(file_path_key):
    ipfs_id = open(f'{IPFS_DIR}/ipfs_id.json')
    cad_part_id_dict = json.load(ipfs_id)
    cad_part_id_dict["FilePathKey"] = file_path_key

    return cad_part_id_dict


def output_CAD(cad_part_id_dict):
    bucket = 'cats-public'
    file_path_key = cad_part_id_dict["FilePathKey"]
    file_name = file_path_key.split('/')[-1]
    node_storage_key = f'output/df/{file_name}'
    NODE_FILE_PATH = f"{WORK_DIR}/job/{node_storage_key}"
    ipfs_addresses = cad_part_id_dict["Addresses"]
    ip4_tcp_addresses = [x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x)]

    output_key = f'cad-store/cad/cao/parts/{file_name}'
    cad_part_id_dict["output_key"] = output_key

    subprocess.check_call(f"mkdir -p {OUTPUT}".split(' '))
    s3_client.download_file(Bucket=bucket, Key=output_key, Filename=NODE_FILE_PATH)
    ipfs_add = f'ipfs add {OUTPUT}/{file_name}'.split(' ')
    [ipfs_action, cid, _file_name] = subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')

    return {
        'cid': cid,
        'addresses': ip4_tcp_addresses,
        'filename': file_name,
        'action': ipfs_action,
        'file_key': output_key
    }

def save_invoice(invoice_uri):
    subprocess.check_call(f"mkdir -p {INVOICE_DIR}".split(' '))

    def download_s3_folder(bucket_name, s3_folder, local_dir=None):
        """
        Download the contents of a folder directory
        Args:
            bucket_name: the name of the s3 bucket
            s3_folder: the folder path in the s3 bucket
            local_dir: a relative or absolute directory path in the local file system
        """
        bucket = s3_resource.Bucket(bucket_name)
        for obj in bucket.objects.filter(Prefix=s3_folder):
            target = obj.key if local_dir is None \
                else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            if obj.key[-1] == '/':
                continue
            bucket.download_file(obj.key, target)

    bucket = invoice_uri.split('s3a://')[1].split('/')[0]
    prefix = invoice_uri.split('s3a://')[1].split(bucket)[1][1:]
    download_s3_folder(bucket, prefix, INVOICE_DIR)

    ipfs_add = f'ipfs add -r {INVOICE_DIR}'.split(' ')
    subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')[0]
    invoice_cid_cmd = f'ipfs add -Qr --only-hash {INVOICE_DIR}'.split(' ')
    invoice_cid = subprocess.check_output(invoice_cid_cmd).decode('ascii').replace('\n', '').split(' ')[0]

    ipfs_id = open(f'{IPFS_DIR}/ipfs_id.json')
    ipfs_addresses = json.load(ipfs_id)["Addresses"]
    ip4_tcp_addresses = [x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x)]

    return (invoice_cid, ip4_tcp_addresses)

def cad_invoicing(file_path_key):
    return output_CAD(link_ipfs_id(file_path_key))


def upload_files(path, bucket_name):
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                bucket.put_object(Key=full_path[len(path) + 1:], Body=data)


def _connect(addresses):
    for address in addresses:
        output = subprocess.check_output(f"ipfs swarm connect {address}", shell=True) \
            .decode('ascii').replace('\n', '').split(' ')
        if output[2] == 'success':
            return address
        else:
            return None

def get_bom(x):
    bom_cid, addresses = x[0], x[1]
    subprocess.check_call(f"mkdir -p {INPUT_DIR}".split(' '))
    os.chdir(INPUT_DIR)

    _connect(addresses)
    output = subprocess.check_output(f"ipfs get {bom_cid}".split(' ')).decode('ascii').replace('\n', '')
    subprocess.check_call(f"mv {bom_cid} bom.json".split(' '))
    bom_file = open(f'{INPUT_DIR}/bom.json')
    bom = json.load(bom_file) #["addresses"]
    return bom
    # for filename in os.listdir(INVOICE_DIR):
    #     try:
    #         file = open(filename, "rb")
    #         s3_client.upload_fileobj(file, Bucket=bucket, Key=prefix)
    #         file.close()
    #         return uri
    #     except Exception as e:
    #         file.close()
    #         return uri


def transfer_invoice(bom):
    invoice_uri = 's3a://cats-public/cad-store/cad/input/invoice'
    subprocess.check_call(f"mkdir -p {INPUT_DIR}".split(' '))

    os.chdir(INPUT_DIR)
    invoice_cid = bom['invoice_cid']
    # subprocess.check_output(f"ipfs get {invoice_cid}".split(' ')).decode('ascii').replace('\n', '')
    subprocess.call(f"ipfs get {invoice_cid}".split(' '))
    time.sleep(15)
    subprocess.call(f"mv {invoice_cid} invoice".split(' '))
    time.sleep(15)

    bom['invoice_uri'] = invoice_uri
    bucket = invoice_uri.split('s3a://')[1].split('/')[0]
    prefix = invoice_uri.split('s3a://')[1].split(bucket)[1][1:]
    INVOICE_DIR = f'{INPUT_DIR}/invoice' # ToDo: disambiguate
    os.chdir(INVOICE_DIR)
    filenames = os.listdir(INVOICE_DIR)
    for filename in filenames:
        file = open(filename, "rb")
        s3_client.upload_fileobj(file, Bucket=bucket, Key=prefix + f'/{filename}')

    return bom


def save_tranformer(transform_uri):
    # 's3a://cats-public/cad-store/cad/transformation/transform.py'
    transform_bucket = transform_uri.split('s3a://')[-1].split('/')[0]
    transform_key = transform_uri.split('s3a://')[-1].split(transform_bucket)[-1][1:]
    transform_filename = transform_key.split('/')[-1]
    NODE_FILE_PATH = f"{TRANSFORM_DIR}/{transform_filename}"

    subprocess.check_call(f"mkdir -p {TRANSFORM_DIR}".split(' '))
    # if doesnt exist
    s3_client.download_file(Bucket=transform_bucket, Key=transform_key, Filename=NODE_FILE_PATH)
    ipfs_add = f'ipfs add {NODE_FILE_PATH}'.split(' ')
    [_, cid, _file_name] = subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')

    partial_bom = {
        'transform_cid': cid,
        'transform_uri': transform_uri,
        'transform_filename': transform_filename,
        'transform_node_path': NODE_FILE_PATH
    }
    return partial_bom

def save_invoice2(invoice_uri):
    INVOICE_DIR = f"{WORK_DIR}/job/input/invoice" # ToDo: disambiguate
    bucket = invoice_uri.split('s3a://')[1].split('/')[0]
    prefix = invoice_uri.split('s3a://')[1].split(bucket)[1][1:]
    uri = 's3a://' + bucket + prefix
    for filename in os.listdir(INVOICE_DIR):
        try:
            file = open(filename, "rb")
            s3_client.upload_fileobj(file, Bucket=bucket, Key=prefix)
            file.close()
            return uri
        except Exception as e:
            file.close()
            return uri

def content_address_transformer_on_driver(self, bom):
    if bom['transformer_uri'] is not None:
        TMP_DIR = '/tmp'
        self.transformer_uri = bom['transformer_uri']

        transform_bucket = self.transformer_uri.split('s3a://')[-1].split('/')[0]
        transform_key = self.transformer_uri.split('s3a://')[-1].split(transform_bucket)[-1][1:]
        transform_filename = transform_key.split('/')[-1]
        NODE_FILE_PATH = f"{TMP_DIR}/{transform_filename}"

        subprocess.check_call(f"mkdir -p {TMP_DIR}".split(' '))
        # if doesnt exist
        s3_client.download_file(Bucket=transform_bucket, Key=transform_key, Filename=NODE_FILE_PATH)
        ipfs_add = f'ipfs add {NODE_FILE_PATH}'.split(' ')
        [ipfs_action, cid, _file_name] = subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')

        with open(f'{TMP_DIR}/ipfs_id.json', 'w') as fp:
            pass
        fp.close()
        os.chdir(TMP_DIR)
        subprocess.check_output(f'ipfs id > ipfs_id.json', shell=True)
        ipfs_id_file = open(f'ipfs_id.json')
        ipfs_addresses = json.load(ipfs_id_file)["Addresses"]
        ipfs_id_file.close()
        ip4_tcp_addresses = [x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x)]

        bom['action'] = ipfs_action
        bom['transform_cid'] = cid
        bom['transformer_addresses'] = ip4_tcp_addresses
        bom['transform_filename'] = transform_filename
        bom['transform_node_path'] = NODE_FILE_PATH
    else:
        bom['transform_cid'] = ''
        bom['transform_filename'] = ''
        bom['transform_node_path'] = ''
        bom['transform_uri'] = ''
    return bom