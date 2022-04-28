import os
from pycats import CATS_HOME
from pycats.factory import Factory
from pycats.function.infrafunction.plant.spark import lazy_SparkSession as lazy_CatSession

CAT_APP_HOME = f"{CATS_HOME}/apps/cat1/cat.py"
TRANSFORM_SOURCE = f"{CATS_HOME}/apps/cat1/transform.py"
TRANSFORM_DEST = 's3://cats-public/cad-store/cad/transformation/transform.py'
tf_script = f'{CATS_HOME}/cluster/tf_cluster_setup.sh'
tf_cmd = f"bash {tf_script}"
catFactory = Factory(
    plantSession=lazy_CatSession,
    DRIVER_IPFS_DIR=f'{CATS_HOME}/cadStore',
    terraform_cmd=tf_cmd,
    terraform_file=f'{CATS_HOME}/main.tf',
    SPARK_HOME=os.getenv('SPARK_HOME'),
    CAT_APP_HOME=CAT_APP_HOME,
    TRANSFORM_SOURCE=TRANSFORM_SOURCE,
    TRANSFORM_DEST=TRANSFORM_DEST
)