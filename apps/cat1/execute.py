from pycats.utils import execute
from pycats.factory.spark import spark_submit

# For Project CI/CD
def build_software():
    build_block = f"""
    pip3 install -r requirements.txt
    python3 setup.py sdist bdist_wheel
    pip3 install dist/pycats-0.0.0-py3-none-any.whl --force-reinstall
    venv-pack -o venv.tar.gz --force
    """
    build_cmds = [i for i in build_block.split("\n") if i]
    for cmd in build_cmds:
        for path in execute(cmd):
            print(path, end="")
    return build_cmds

HOME = '/home/jjodesty'
SPARK_HOME = '/usr/local/spark'
CATS_HOME = f'{HOME}/Projects/Research/cats/apps/cat1'
CAT_APP_HOME = f"{CATS_HOME}/cat.py"
TRANSFORM_SOURCE = f'{CATS_HOME}/transform.py'
TRANSFORM_DEST = 's3://cats-public/cad-store/cad/transformation/transform.py'
build_software()
spark_submit(SPARK_HOME, CAT_APP_HOME, TRANSFORM_SOURCE, TRANSFORM_DEST)

# 15:35:43
# 15:37:28