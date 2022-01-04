import os
from pyspark.sql import SparkSession

# InfraStructure
SparkSession: SparkSession = SparkSession \
    .builder \
    .master("k8s://https://192.168.49.2:8443") \
    .appName("sparkCAT") \
    .config("spark.executor.instances","2") \
    .config("spark.executor.memory", "2g") \
    .config("spark.kubernetes.container.image", "pyspark/spark-py:latest") \
    .config("spark.kubernetes.container.image.pullPolicy", "Never") \
    .config("spark.kubernetes.authenticate.driver.serviceAccountName", "spark") \
    .config("spark.kubernetes.executor.deleteOnTermination", "true") \
    .config("spark.kubernetes.executor.secrets.aws-access", "/etc/secrets") \
    .config("spark.kubernetes.executor.secretKeyRef.AWS_ACCESS_KEY_ID", "aws-access:AWS_ACCESS_KEY_ID") \
    .config("spark.kubernetes.executor.secretKeyRef.AWS_SECRET_ACCESS_KEY", "aws-access:AWS_SECRET_ACCESS_KEY") \
    .config("spark.hadoop.fs.s3a.access.key", os.getenv('AWS_ACCESS_KEY_ID')) \
    .config("spark.hadoop.fs.s3a.secret.key", os.environ.get('AWS_SECRET_ACCESS_KEY')) \
    .config("spark.kubernetes.file.upload.path", "s3a://cats-storage/input/") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.fast.upload", "true") \
    .config("spark.driver.extraJavaOptions", "'-Divy.cache.dir=/tmp -Divy.home=/tmp'") \
    .config("spark.pyspark.driver.python", "/home/jjodesty/Projects/Research/cats/venv/bin/python") \
    .getOrCreate()