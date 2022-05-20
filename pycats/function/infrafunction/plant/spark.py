import os
from pyspark.sql import SparkSession
from pycats import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from pycats.utils import execute
from pycats.structure.plant.spark import CATS_HOME


SparkSessionConfig = {
    'spark.master': 'k8s://https://192.168.49.2:8443',
    'spark.app.name': 'sparkCAT',
    'spark.executor.instances': '4',
    'spark.executor.memory': '5g',
    'spark.kubernetes.container.image': 'pyspark/spark-py:latest',
    'spark.kubernetes.container.image.pullPolicy': 'Never',
    'spark.kubernetes.authenticate.driver.serviceAccountName': 'spark',
    'spark.kubernetes.executor.deleteOnTermination': 'true',
    'spark.kubernetes.executor.secrets.aws-access': '/etc/secrets',
    'spark.kubernetes.executor.secretKeyRef.AWS_ACCESS_KEY_ID': 'aws-access:AWS_ACCESS_KEY_ID',
    'spark.kubernetes.executor.secretKeyRef.AWS_SECRET_ACCESS_KEY': 'aws-access:AWS_SECRET_ACCESS_KEY',
    'spark.hadoop.fs.s3a.access.key': AWS_ACCESS_KEY_ID,
    'spark.hadoop.fs.s3a.secret.key': AWS_SECRET_ACCESS_KEY,
    'spark.kubernetes.file.upload.path': 's3a://cats-storage/input/',
    'spark.hadoop.fs.s3a.impl': 'org.apache.hadoop.fs.s3a.S3AFileSystem',
    'spark.hadoop.fs.s3a.fast.upload': 'true',
    'spark.driver.extraJavaOptions': "'-Divy.cache.dir=/tmp -Divy.home=/tmp'",
    # 'spark.pyspark.driver.python': f'{CATS_HOME}/venv/bin/python',
    'log4j2.formatMsgNoLookups': 'true'
}

class CATSession():
    def __init__(self,
        plant_session_config: dict = SparkSessionConfig,
    ):
        self.plant_session_config = plant_session_config
        self.plantSession = None

    def lazy_SparkSession(self, config_dict: dict = None):
        if config_dict is None:
            config_dict = self.plant_session_config
        # os.environ['PYSPARK_DRIVER_PYTHON'] = "python"
        os.environ['PYSPARK_PYTHON'] = "./environment/bin/python"
        # config_dict['spark.pyspark.driver.python'] = "python"
        # config_dict['spark.pyspark.python'] = "./environment/bin/python"
        # config_dict['spark.archives'] = "venv.tar.gz#environment"
        SparkSessionBuilder: SparkSession = SparkSession \
            .builder
        for k, v in config_dict.items():
            catSparkSession = SparkSessionBuilder.config(k, v)
        self.plantSession = catSparkSession.getOrCreate()
        return self.plantSession


# factory method
def spark_submit(
        SPARK_HOME,
        CAT_APP_HOME,
        TRANSFORM_SOURCE=None,
        TRANSFORM_DESTINATION=None
):
    # env_vars = os.environ.copy()
    # env_vars['PYSPARK_DRIVER_PYTHON'] = 'python'
    # env_vars['PYSPARK_PYTHON'] = './environment/bin/python'

    # os.environ['PYSPARK_DRIVER_PYTHON'] = "python"
    # os.environ['PYSPARK_PYTHON'] = "./environment/bin/python"
    # execute('export PYSPARK_DRIVER_PYTHON=python')
    # execute('export PYSPARK_PYTHON=./environment/bin/python')
    spark_submit_block = f"""
    {SPARK_HOME}/bin/spark-submit \
    --packages com.amazonaws:aws-java-sdk:1.11.375 \
    --packages org.apache.hadoop:hadoop-aws:3.2.0 \
    --archives venv.tar.gz#environment file://{CAT_APP_HOME}
    """
    spark_submit_cmds = [i for i in spark_submit_block.split("\n") if i]

    if TRANSFORM_SOURCE is not None or TRANSFORM_DESTINATION is not None:
        aws_cp = f'aws s3 cp {TRANSFORM_SOURCE} {TRANSFORM_DESTINATION}'
        spark_submit_cmds = [aws_cp] + spark_submit_cmds
    for cmd in spark_submit_cmds:
        # for path in execute(cmd, env_vars):
        for path in execute(cmd):
            print(path, end="")
    # pprint(spark_submit_cmds)
    return spark_submit_cmds

"""
pip3 install -r requirements.txt
python3 setup.py sdist bdist_wheel
pip3 install dist/pycats-0.0.0-py3-none-any.whl --force-reinstall
venv-pack -o venv.tar.gz --force
spark-submit  \
--packages com.amazonaws:aws-java-sdk:1.11.375 \
--packages org.apache.hadoop:hadoop-aws:3.2.0  \
--archives venv.tar.gz#environment file:///home/jjodesty/Projects/Research/cats/apps/cat0/id_content.py
"""

