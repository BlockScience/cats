from pycats.utils import build_software
from pycats.function.infrafunction.plant.spark import spark_submit


HOME = '/home/jjodesty'
SPARK_HOME = '/usr/local/spark'
CATS_HOME = f'{HOME}/Projects/Research/cats/apps/cat0'
CAT_APP_HOME = f"{CATS_HOME}/id_content.py"
build_software()
spark_submit(SPARK_HOME, CAT_APP_HOME)

# 15:35:43
# 15:37:28