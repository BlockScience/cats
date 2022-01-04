import json
import os, subprocess, boto3
# ToDo: place imports that can be serialized here
# ToDo: isolate repeat functionality due to venv
import time

s3 = boto3.client(
    's3',
    region_name='us-east-2',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)


def get_s3_keys(bucket, part_path):
    """Get a list of keys in an S3 bucket."""
    keys = []
    # resp = s3.list_objects_v2(Bucket=bucket, Prefix='input/df/')
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=part_path)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    if part_path in keys:
        keys.remove(part_path)
    return keys


# def content_address_tranformation(transform_uri):
def content_address_tranformer(transform_uri):
    # import s3 from package here
    import boto3, json
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    WORK_DIR = '/opt/spark/work-dir'
    TRANSFORM_DIR = f"{WORK_DIR}/job/transformation"
    IPFS_DIR = f'{WORK_DIR}/ipfs'
    # 's3a://cats-public/cad-store/cad/transformation/transform.py'
    transform_bucket = transform_uri.split('s3a://')[-1].split('/')[0]
    transform_key = transform_uri.split('s3a://')[-1].split(transform_bucket)[-1][1:]
    transform_filename = transform_key.split('/')[-1]
    NODE_FILE_PATH = f"{TRANSFORM_DIR}/{transform_filename}"

    subprocess.check_call(f"mkdir -p {TRANSFORM_DIR}".split(' '))
    # if doesnt exist
    s3.download_file(Bucket=transform_bucket, Key=transform_key, Filename=NODE_FILE_PATH)
    ipfs_add = f'ipfs add {NODE_FILE_PATH}'.split(' ')
    [ipfs_action, cid, _file_name] = subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')

    ipfs_id = open(f'{IPFS_DIR}/ipfs_id.json')
    ipfs_addresses = json.load(ipfs_id)["Addresses"]
    ip4_tcp_addresses = [x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x)]

    partial_bom =  {
        'action': ipfs_action,
        'transform_cid': cid,
        'transform_uri': transform_uri,
        'addresses': ip4_tcp_addresses,
        'transform_filename': transform_filename,
        'transform_node_path': NODE_FILE_PATH
    }
    return partial_bom

def save_bom(bom_type: str = 'cao'):
    def f(partial_bom):
        import json
        WORK_DIR = '/opt/spark/work-dir'
        BOM_DIR = f"{WORK_DIR}/job/bom"
        BOM_FILE = f'{BOM_DIR}/{bom_type}_bom.json'
        subprocess.check_call(f"mkdir -p {BOM_DIR}".split(' '))
        with open(BOM_FILE, 'w') as fp:
            json.dump(partial_bom, fp)
        ipfs_add = f'ipfs add {BOM_FILE}'.split(' ')
        [_, bom_cid, _file_name] = subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')
        partial_bom['cad_cid'] = bom_cid
        return partial_bom
    return f

# Ingest
def cad_part_invoice(cad_part_id_dict):
    # import s3 from package here
    import boto3
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    WORK_DIR = '/opt/spark/work-dir'
    INPUT = f"{WORK_DIR}/job/input/df"

    bucket = 'cats-public'
    file_path_key = cad_part_id_dict["FilePathKey"]
    file_name = file_path_key.split('/')[-1]
    NODE_FILE_PATH = f"{WORK_DIR}/job/{file_path_key}"
    ipfs_addresses = cad_part_id_dict["Addresses"]
    ip4_tcp_addresses = [x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x)]

    subprocess.check_call(f"mkdir -p {INPUT}".split(' '))
    s3.download_file(Bucket=bucket, Key=file_path_key, Filename=NODE_FILE_PATH)  # delete after transfer
    ipfs_add = f'ipfs add {INPUT}/{file_name}'.split(' ')
    [ipfs_action, cid, _file_name] = subprocess.check_output(ipfs_add).decode('ascii').replace('\n', '').split(' ')

    return {
        'cid': cid,
        'addresses': ip4_tcp_addresses,
        'filename': file_name,
        'action': ipfs_action,
        'file_key': file_path_key
    }

def ipfs_connect(cad_part_invoice):
    addresses = cad_part_invoice['addresses']
    for address in addresses:
        output = subprocess.check_output(f"ipfs swarm connect {address}".split(' ')) \
            .decode('ascii').replace('\n', '').split(' ')
        if output[2] == 'success':
            cad_part_invoice['connection'] = address
        else:
            cad_part_invoice['connection'] = None
        return cad_part_invoice


def s3_ingest(cad_part_invoice):
    import boto3
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    WORK_DIR = '/opt/spark/work-dir'
    INPUT = f"{WORK_DIR}/job/input/df"


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
            file = open(filename, "rb")
            s3.upload_fileobj(file, Bucket=bucket, Key=key)
            cad_part_invoice['upload_path'] = uri
            return cad_part_invoice
        except Exception as e:
            cad_part_invoice['upload_path'] = str(e)
            return cad_part_invoice



def ipfs_caching(file_path_key):
    return cad_part_invoice(link_ipfs_id(file_path_key))

def cluster_fs_ingest(cad_part_invoice):
    return s3_ingest(ipfs_connect(cad_part_invoice))


# CAD
def get_upload_path(cad_part_invoice):
    return str(cad_part_invoice['upload_path'])


# CAT
def link_ipfs_id(file_path_key):
    import json
    WORK_DIR = '/opt/spark/work-dir'
    IPFS_DIR = f'{WORK_DIR}/ipfs'
    ipfs_id = open(f'{IPFS_DIR}/ipfs_id.json')
    cad_part_id_dict = json.load(ipfs_id)
    cad_part_id_dict["FilePathKey"] = file_path_key

    return cad_part_id_dict


def output_CAD(cad_part_id_dict):
    # import s3 from package here
    import boto3
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    WORK_DIR = '/opt/spark/work-dir'
    OUTPUT = f"{WORK_DIR}/job/output/df"

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
    s3.download_file(Bucket=bucket, Key=output_key, Filename=NODE_FILE_PATH)
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
    s3 = boto3.resource('s3',
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
                        )
    WORK_DIR = '/opt/spark/work-dir'
    INVOICE_DIR = f"{WORK_DIR}/job/invoice"
    IPFS_DIR = f'{WORK_DIR}/ipfs'
    subprocess.check_call(f"mkdir -p {INVOICE_DIR}".split(' '))

    def download_s3_folder(bucket_name, s3_folder, local_dir=None):
        """
        Download the contents of a folder directory
        Args:
            bucket_name: the name of the s3 bucket
            s3_folder: the folder path in the s3 bucket
            local_dir: a relative or absolute directory path in the local file system
        """
        bucket = s3.Bucket(bucket_name)
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
    session = boto3.Session(
        region_name='us-east-2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)

    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                bucket.put_object(Key=full_path[len(path) + 1:], Body=data)


def _connect(addresses):
    for address in addresses:
        output = subprocess.check_output(f"ipfs swarm connect {address}".split(' ')) \
            .decode('ascii').replace('\n', '').split(' ')
        if output[2] == 'success':
            return address
        else:
            return None


def get_bom(x):
    bom_cid, addresses = x[0], x[1]
    WORK_DIR = '/opt/spark/work-dir'
    INPUT_DIR = f"{WORK_DIR}/job/input"
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
    #         s3.upload_fileobj(file, Bucket=bucket, Key=prefix)
    #         file.close()
    #         return uri
    #     except Exception as e:
    #         file.close()
    #         return uri


def transfer_invoice(bom):
    invoice_uri = 's3a://cats-public/cad-store/cad/input/invoice'
    import boto3
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    WORK_DIR = '/opt/spark/work-dir'
    INPUT_DIR = f"{WORK_DIR}/job/input"
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
    INVOICE_DIR = f'{INPUT_DIR}/invoice'
    os.chdir(INVOICE_DIR)
    filenames = os.listdir(INVOICE_DIR)
    for filename in filenames:
        file = open(filename, "rb")
        s3.upload_fileobj(file, Bucket=bucket, Key=prefix+f'/{filename}')

    return bom


def save_tranformer(transform_uri):
    # import s3 from package here
    import boto3, json
    s3 = boto3.client(
        's3',
        region_name='us-east-2',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    WORK_DIR = '/opt/spark/work-dir'
    TRANSFORM_DIR = f"{WORK_DIR}/job/transformation"
    IPFS_DIR = f'{WORK_DIR}/ipfs'
    # 's3a://cats-public/cad-store/cad/transformation/transform.py'
    transform_bucket = transform_uri.split('s3a://')[-1].split('/')[0]
    transform_key = transform_uri.split('s3a://')[-1].split(transform_bucket)[-1][1:]
    transform_filename = transform_key.split('/')[-1]
    NODE_FILE_PATH = f"{TRANSFORM_DIR}/{transform_filename}"

    subprocess.check_call(f"mkdir -p {TRANSFORM_DIR}".split(' '))
    # if doesnt exist
    s3.download_file(Bucket=transform_bucket, Key=transform_key, Filename=NODE_FILE_PATH)
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
    WORK_DIR = '/opt/spark/work-dir'
    INPUT_DIR = f"{WORK_DIR}/job/input"
    INVOICE_DIR = f"{WORK_DIR}/job/input/invoice"
    bucket = invoice_uri.split('s3a://')[1].split('/')[0]
    prefix = invoice_uri.split('s3a://')[1].split(bucket)[1][1:]
    uri = 's3a://' + bucket + prefix
    for filename in os.listdir(INVOICE_DIR):
        try:
            file = open(filename, "rb")
            s3.upload_fileobj(file, Bucket=bucket, Key=prefix)
            file.close()
            return uri
        except Exception as e:
            file.close()
            return uri

# def input2(self, addresses, bom_cid, transformer_uri=None):
#     IPFS_DIR = '/home/jjodesty/Projects/Research/cats/cadStore'
#     import time, subprocess
#     ipfs_daemon = f'ipfs daemon'
#     proc = subprocess.Popen(
#         ipfs_daemon, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
#     )
#     pid = proc.pid
#     time.sleep(15)
#     ipfs_id_cmd = f'ipfs id > {IPFS_DIR}/ipfs_id.json'
#     subprocess.check_call(ipfs_id_cmd, shell=True)
#     ipfs_id = open(f'{IPFS_DIR}/ipfs_id.json')
#     ipfs_addresses = json.load(ipfs_id)["Addresses"]
#     ip4_tcp_addresses = [x for x in ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x)]
#     proc.kill()
#     return ip4_tcp_addresses