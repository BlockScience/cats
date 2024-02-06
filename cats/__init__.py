import os
from os.path import dirname, abspath

CATS_HOME = dirname(dirname(abspath(__file__)))
DATA_HOME = CATS_HOME + '/data'
CWD = os.getcwd()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
