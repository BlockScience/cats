# CAT0: Content-Addresses Dataset
Content-Addresses Dataset as Content-Addressed Input (CAI) by generating initial catBOM used by the subsequent CAT in 
catPipe (CAT1) as form of input:
* CAT0 generates a catBOM by Content Identifying (CIDing) an Invoice of Data Partition Transactions, a Data 
    Transformation, and itself
* CAT0 decentralizes data by CIDing with IPFS from a centralized source AWS s3
* **Examples:**
  1. **Execution:** Open terminal session, activate pre-created virtual environment, and execute CAT
     1. Builds (Optional for development), Terraforms minikube K8s cluster & builds Spark Image, and executes a CAT
     ```bash
     cd <parrent directory>/cats
     source ./venv/bin/activate
     python apps/cat0/execute.py
     ```
     2. Deactivate Virtual Environment (Optional): `deactivate`
     ```bash
     (venv) $ deactivate
     $
     ```
  2. **CAT0 Application:** Content-Address Input with a CAT
     1. **[Module Example:](cats/apps/cat0/__init__.py)**: Instantiate `catFactory` within `apps/cat0/__init__.py`
       ```python
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
       SparkSessionConfig['spark.pyspark.driver.python'] = f'{CATS_HOME}/venv/bin/python'

       tf_script = f'{CATS_HOME}/cluster/tf_cluster_setup.sh'
       tf_cmd = f"bash {tf_script}"
       catFactory = Factory(
           plantConfig=SparkSessionConfig, # Configuration of Plant Session
           terraform_cmd=tf_cmd, # Bash script to Terraform Plant Cluster (Kubernetes Pod Group)
           terraform_file=f'{CATS_HOME}/main.tf', # Terraform file to CID for catBOM
           SPARK_HOME=SPARK_HOME, # Plant Home Environmental Variable
           CAT_APP_HOME=f"{CATS_HOME}/apps/cat0/id_content.py" # Plant Application
       )
       ```
     2. Content-Address Input with CAT `Processor` produced by `catFactory` within `apps/cat0/id_content.py`
          1. Process Input
             * **input_data_uri** - URI of Input data
             * **cai_partitions** - Partition count of an Invoice/CAD representing the amount of concurrent threads 
             used to generate it
             * Process Output URIs as Input
                1. Invoice / Content-Addressed Dataset (CAD)
                   * **invoice_uri** - URI of Invoice/CAD
                2. CAT Bill Of Materials (BOM) 
                   * **bom_write_path_uri** - URI of BOM
                   * **output_data_uri** - URI for subsequent CAT Output Data
                   * **transformer_uri** - URI of subsequent CAT data transformation (Python / (Spark/ANSII) SQL)
                   (**[Data Transformation Example](cats/catStore/cats-public/cad-store/cad/transformation/transform.py)**)
          2. **[Module Example:](cats/apps/cat0/id_content.py)**
          ```python
          from pycats import CATS_HOME, CATSTORE
          from apps.cat0 import catFactory
          from pycats.function.process.cat import Processor

          cat: Processor = catFactory.init_processor(ipfs_daemon=True)
          local_bom_write_path = f'{CATS_HOME}/catStore/bom.json',
          cai_bom, input_cad_invoice = cat.content_address_input(
              input_data_uri=f'{CATS_HOME}/catStore/cats-public/input/df', # I
              invoice_uri=f'{CATSTORE}/cad/cai/invoices', # O
              bom_write_path_uri='s3://cats-public/cad-store/cad/cai/bom/bom.json', # O
              output_data_uri='s3://cats-public/cad-store/cad/cao/data', # I/O
              transformer_uri=f'{CATSTORE}/cad/transformation/transform.py', # I/O
              cai_partitions=1
          )
          ```
     
  3. **CAT0 Process Output**
     ```bash
     # Invoice / Content-Addressed Dataset (CAD) [Single Partition]
     +------+--------------------+--------------------+--------------------+---------------+
     |action|           addresses|                 cid|            file_key|       filename|
     +------+--------------------+--------------------+--------------------+---------------+
     | added|[/ip4/172.17.0.5/...|QmSNBaSYYmvmAvWmV...|input/df_json_0/p...|part-00000.json|
     +------+--------------------+--------------------+--------------------+---------------+

     # CAI BOM
     {'action': 'added',
     'bom_cid': 'QmQaYFQ9naBFSTthjiyFLPfu8CnVNf6c2Ju9PbyhyZLqmb',
     'bom_uri': 's3://cats-public/cad-store/cad/cai/bom/bom.json',
     'cai_data_uri': 's3://cats-public/cad-store/cad/cao/data',
     'cai_invoice_uri': 's3://cats-public/cad-store/cad/cai/invoices',
     'cai_part_cids': ['QmSNBaSYYmvmAvWmVpXFSiDfr5u1RW3EZwSUYkibwbG6BZ'],
     'input_bom_cid': '',
     'log_write_path_uri': 's3://cats-public/cad-store/cad/cai/bom/bom_cat_log.json',
     'terraform_cid': 'QmcRntT77xT94evHfvtgg2T1Q9bXJ9m6fkoxGwaWawkZD2',
     'terraform_file': '/home/jjodesty/Projects/Research/cats/main.tf',
     'terraform_filename': 'main.tf',
     'terraform_node_path': '/tmp/main.tf',
     'transform_cid': 'QmRL4zysjoDURNWqCehR1mNCDcMVG1oDpKvguJSmnyhb1e',
     'transform_filename': 'transform.py',
     'transform_node_path': '/opt/spark/work-dir/job/transformation/transform.py',
     'transform_uri': 's3://cats-public/cad-store/cad/transformation/transform.py',
     'transformer_uri': 's3://cats-public/cad-store/cad/transformation/transform.py'}

     # CAT log: Addresses
     {'addresses': ['/ip4/70.107.79.74/tcp/29347/p2p/12D3KooWNZ9C3mHTwZMYwnwcYWn8wbEkNRRFS4Ze27QnuK1jAB1R',
                      '/ip4/172.17.0.3/tcp/4001/p2p/12D3KooWNZ9C3mHTwZMYwnwcYWn8wbEkNRRFS4Ze27QnuK1jAB1R'],
     'terraform_addresses': ['/ip4/192.168.1.27/tcp/4001/p2p/12D3KooWMqjgHjaxpHqQUuBrzPJS7nM1QLQ2tTHZoLYEVVqEbdyD',
                                '/ip4/70.107.79.74/tcp/38211/p2p/12D3KooWMqjgHjaxpHqQUuBrzPJS7nM1QLQ2tTHZoLYEVVqEbdyD'],
     'transformer_addresses': ['/ip4/172.17.0.4/tcp/4001/p2p/12D3KooWPuCynRm1Xm1tTxzcQatwHjajNteTPdcczU7h1EG2osyG',
     '/ip4/70.107.79.74/tcp/26037/p2p/12D3KooWPuCynRm1Xm1tTxzcQatwHjajNteTPdcczU7h1EG2osyG']} 
     ```