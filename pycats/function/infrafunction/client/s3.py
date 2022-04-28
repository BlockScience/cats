import json, subprocess
from pycats.function.process.utils import s3_client, s3_resource, s3Utils


class Client(s3Utils):
    def __init__(self):
        self.s3_client = s3_client
        s3Utils.__init__(self)

    def get_s3_keys(self, bucket, part_path):
        """Get a list of keys in an S3 bucket."""
        keys = []
        # resp = self.client.list_objects_v2(Bucket=bucket, Prefix='input/df/')
        resp = self.s3_client.list_objects_v2(Bucket=bucket, Prefix=part_path)
        for obj in resp['Contents']:
            keys.append(obj['Key'])
        if part_path in keys:
            keys.remove(part_path)
        return keys

    def aws_cli_cp(self, source, destination):
        aws_cp = f'aws s3 cp {source} {destination}'
        subprocess.check_call(aws_cp.split(' '))

    def boto3_cp(self, source, destination):
        source_bucket, source_key = self.get_s3_bucket_key_pair(source)
        destination_bucket, destination_key = self.get_s3_bucket_key_pair(destination)
        copy_source = {
            'Bucket': source_bucket,
            'Key': source_key
        }
        s3_resource.meta.client.copy(copy_source, destination_bucket, destination_key)

    def download_dict_file(self, s3_filepath, local_dict_filepath):
        bucket, key = self.get_s3_bucket_key_pair(s3_filepath)
        self.s3_client.download_file(Bucket=bucket, Key=key, Filename=local_dict_filepath)
        with open(local_dict_filepath) as dict_file:
            pyDict = json.load(dict_file)
        dict_file.close()
        return pyDict
