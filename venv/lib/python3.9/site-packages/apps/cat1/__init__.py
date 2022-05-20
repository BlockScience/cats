from pycats.factory import Factory
from pycats.function.infrafunction.plant.spark import SparkSessionConfig
from pycats import CATS_HOME, SPARK_HOME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, CATSTORE

# Configure Plant Session (Apache Spark Session)
SparkSessionConfig['spark.app.name'] = 'CAT'
SparkSessionConfig['spark.executor.instances'] = '3'
SparkSessionConfig['spark.executor.memory'] = '2g'
SparkSessionConfig['spark.kubernetes.executor.deleteOnTermination'] = 'true'
SparkSessionConfig['spark.hadoop.fs.s3a.access.key'] = AWS_ACCESS_KEY_ID
SparkSessionConfig['spark.hadoop.fs.s3a.secret.key'] = AWS_SECRET_ACCESS_KEY
SparkSessionConfig['spark.kubernetes.file.upload.path'] = 's3a://cats-storage/input/'
SparkSessionConfig['spark.pyspark.driver.python'] = f'{CATS_HOME}/venv/bin/python'

CAT_APP_HOME = f"{CATS_HOME}/apps/cat1/cat.py"
TRANSFORM_SOURCE = f'{CATSTORE}/cad/transformation/transform.py'
TRANSFORM_DEST = 's3://cats-public/cad-store/cad/transformation/transform.py'
tf_script = f'{CATS_HOME}/cluster/tf_cluster_setup.sh'
tf_cmd = f"bash {tf_script}"
catFactory = Factory(
    plantConfig=SparkSessionConfig, # Configuration of Plant Session
    DRIVER_IPFS_DIR=f'{CATS_HOME}/catStore', # Local / Node CAT storage
    terraform_cmd=tf_cmd, # Bash script to Terraform Plant Cluster (Kubernetes Pod Group)
    terraform_file=f'{CATS_HOME}/main.tf', # Terraform file to CID for catBOM
    SPARK_HOME=SPARK_HOME, # Plant Home Environmental Variable
    CAT_APP_HOME=CAT_APP_HOME, # Plant Application
    TRANSFORM_SOURCE=TRANSFORM_SOURCE, # Local / Node data transformation module for CAT
    TRANSFORM_DEST=TRANSFORM_DEST # Cluster file system URI data transformation module for CAT will be written to
)