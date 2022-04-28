import os
from pycats import CATS_HOME
from pycats.factory import Factory
from pycats.function.infrafunction.plant.spark import lazy_SparkSession as lazy_CatSession

tf_script = f'{CATS_HOME}/cluster/tf_cluster_setup.sh'
tf_cmd = f"bash {tf_script}"
catFactory = Factory(
    plantSession=lazy_CatSession,
    terraform_cmd=tf_cmd,
    terraform_file=f'{CATS_HOME}/main.tf',
    SPARK_HOME=os.getenv('SPARK_HOME'),
    CAT_APP_HOME=f"{CATS_HOME}/apps/cat0/id_content.py"
)