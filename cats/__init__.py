import os
from os.path import dirname, abspath
CATS_HOME = dirname(dirname(abspath(__file__)))
DATA_HOME = CATS_HOME + '/data'
# SPARK_HOME = os.getenv('SPARK_HOME')
# DRIVER_IPFS_DIR = f'{CATS_HOME}/catStore'
# CATSTORE = f'{CATS_HOME}/catStore/cats-public/cad-store'
# ToDo: change w3 access
CWD = os.getcwd()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')