from pycats.factory import Factory
from pycats.function.infrafunction.plant.spark import SparkSessionConfig
from pycats import CATS_HOME, SPARK_HOME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# Configure Plant Session (Apache Spark Session)
SparkSessionConfig['spark.app.name'] = 'CAD'
SparkSessionConfig['spark.executor.instances'] = '3'
SparkSessionConfig['spark.executor.memory'] = '1g'
SparkSessionConfig['spark.kubernetes.executor.deleteOnTermination'] = 'true'
SparkSessionConfig['spark.hadoop.fs.s3a.access.key'] = AWS_ACCESS_KEY_ID
SparkSessionConfig['spark.hadoop.fs.s3a.secret.key'] = AWS_SECRET_ACCESS_KEY
SparkSessionConfig['spark.kubernetes.file.upload.path'] = 's3a://cats-storage/input/'
SparkSessionConfig['spark.pyspark.driver.python'] = f'{CATS_HOME}/venv/bin/py thon'

tf_script = f'{CATS_HOME}/cluster/tf_cluster_setup.sh'
tf_cmd = f"bash {tf_script}"
catFactory = Factory(
    plantConfig=SparkSessionConfig, # Configuration of Plant Session
    terraform_cmd=tf_cmd, # Bash script to Terraform Plant Cluster (Kubernetes Pod Group)
    terraform_file=f'{CATS_HOME}/main.tf', # Terraform file to CID for catBOM
    SPARK_HOME=SPARK_HOME, # Plant Home Environmental Variable
    CAT_APP_HOME=f"{CATS_HOME}/apps/cat0/id_content.py" # Plant Application
)