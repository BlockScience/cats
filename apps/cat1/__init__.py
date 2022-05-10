from pycats.factory import Factory
from pycats.function.infrafunction.plant.spark import SparkSessionConfig
from pycats import CATS_HOME, SPARK_HOME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

SparkSessionConfig['spark.app.name'] = 'CAT'
SparkSessionConfig['spark.executor.instances'] = '4'
SparkSessionConfig['spark.executor.memory'] = '5g'
SparkSessionConfig['spark.kubernetes.executor.deleteOnTermination'] = 'true'
SparkSessionConfig['spark.hadoop.fs.s3a.access.key'] = AWS_ACCESS_KEY_ID
SparkSessionConfig['spark.hadoop.fs.s3a.secret.key'] = AWS_SECRET_ACCESS_KEY
SparkSessionConfig['spark.kubernetes.file.upload.path'] = 's3a://cats-storage/input/'
SparkSessionConfig['spark.pyspark.driver.python'] = f'{CATS_HOME}/venv/bin/python'

CAT_APP_HOME = f"{CATS_HOME}/apps/cat1/cat.py"
TRANSFORM_SOURCE = f"{CATS_HOME}/apps/cat1/transform.py"
TRANSFORM_DEST = 's3://cats-public/cad-store/cad/transformation/transform.py'
tf_script = f'{CATS_HOME}/cluster/tf_cluster_setup.sh'
tf_cmd = f"bash {tf_script}"
catFactory = Factory(
    plantConfig=SparkSessionConfig,
    DRIVER_IPFS_DIR=f'{CATS_HOME}/catStore',
    terraform_cmd=tf_cmd,
    terraform_file=f'{CATS_HOME}/main.tf',
    SPARK_HOME=SPARK_HOME,
    CAT_APP_HOME=CAT_APP_HOME,
    TRANSFORM_SOURCE=TRANSFORM_SOURCE,
    TRANSFORM_DEST=TRANSFORM_DEST
)