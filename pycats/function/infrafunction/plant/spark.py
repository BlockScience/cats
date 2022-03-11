import os
from pycats.utils import execute

# factory method
def spark_submit(
        SPARK_HOME,
        CAT_APP_HOME,
        TRANSFORM_SOURCE=None,
        TRANSFORM_DESTINATION=None
):
    env_vars = os.environ.copy()
    env_vars['PYSPARK_DRIVER_PYTHON'] = 'python'
    env_vars['PYSPARK_PYTHON'] = './environment/bin/python'
    spark_submit_block = f"""
    {SPARK_HOME}/bin/spark-submit \
    --packages com.amazonaws:aws-java-sdk:1.11.375 \
    --packages org.apache.hadoop:hadoop-aws:3.2.0 \
    --archives venv.tar.gz#environment file://{CAT_APP_HOME}
    """
    spark_submit_cmds = [i for i in spark_submit_block.split("\n") if i]

    if TRANSFORM_SOURCE is not None or TRANSFORM_DESTINATION is not None:
        aws_cp = f'aws s3 cp {TRANSFORM_SOURCE} {TRANSFORM_DESTINATION}'
        spark_submit_cmds = [aws_cp] + spark_submit_cmds
    for cmd in spark_submit_cmds:
        for path in execute(cmd, env_vars):
            print(path, end="")
    # pprint(spark_submit_cmds)
    return spark_submit_cmds

"""
pip3 install -r requirements.txt
python3 setup.py sdist bdist_wheel
pip3 install dist/pycats-0.0.0-py3-none-any.whl --force-reinstall
venv-pack -o venv.tar.gz --force
spark-submit  \
--packages com.amazonaws:aws-java-sdk:1.11.375 \
--packages org.apache.hadoop:hadoop-aws:3.2.0  \
--archives venv.tar.gz#environment file:///home/jjodesty/Projects/Research/cats/apps/cat0/id_content.py
"""

