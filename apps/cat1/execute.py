import os
from pycats.utils import build_software
from pycats.function.infrafunction.plant.spark import spark_submit


# HOME = '/home/jjodesty'
# SPARK_HOME = '/usr/local/spark'
# CATS_HOME = f'{HOME}/Projects/Research/cats/apps/cat1'
# CAT_APP_HOME = f"{CATS_HOME}/cat.py"
# TRANSFORM_SOURCE = f'{CATS_HOME}/transform.py'

# HOME = os.getenv('HOME')
SPARK_HOME = os.getenv('SPARK_HOME')
CATS_HOME = os.getenv('CATS_HOME')
CAT_APP_HOME = f"{CATS_HOME}/apps/cat1/cat.py"
TRANSFORM_SOURCE = f"{CATS_HOME}/apps/cat1/transform.py"
TRANSFORM_DEST = 's3://cats-public/cad-store/cad/transformation/transform.py'
build_software()
spark_submit(SPARK_HOME, CAT_APP_HOME, TRANSFORM_SOURCE, TRANSFORM_DEST)

# 15:35:43
# 15:37:28