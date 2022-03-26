import os

from pycats.utils import build_software
from pycats.function.infrafunction.plant.spark import spark_submit


# HOME = '/home/jjodesty'
# SPARK_HOME = '/usr/local/spark'
# CATS_HOME = f'{HOME}/Projects/Research/cats/apps/cat0'
# CAT_APP_HOME = f"{CATS_HOME}/id_content.py"

# HOME = os.getenv('HOME')
SPARK_HOME = os.getenv('SPARK_HOME')
CATS_HOME = os.getenv('CATS_HOME')
CAT_APP_HOME = f"{CATS_HOME}/apps/cat0/id_content.py"
build_software()
spark_submit(SPARK_HOME, CAT_APP_HOME)

# 15:35:43
# 15:37:28