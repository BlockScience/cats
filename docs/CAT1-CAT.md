# CAT1: Content-Addresses Transform
1. **CAT1:** Content-Address Transform Dataset given CAT0 BOM to produce new CAO & catBOM for subsequent CAT 
   * CAT1 is the primary data transformation UI for a CAT** representing 0 to n CATs and illustrates a CATpipe
     * CATs uses the catBOM as input and output enabling users to reproduce I/O data using a Content Identified (CIDed) 
     Invoice containing Data Partition Transactions and a CIDed Data Transformation 
       * These transactions are records of data partition add or get command executions of an IPFS client that provide 
       access to Output Data and Transformations generating via CIDs to be accessed on the IPFS p2p network
         * It can also provide access via s3 URIs
   * **Examples:**
     1. **Execution:** 
        1. Builds (Optional for development), Terraforms minikube K8s cluster & builds Spark Image, and executes a CAT
              ```bash
              cd <parent directory>/cats
              source ./venv/bin/activate
              python3.9 apps/cat1/execute.py
              ```
              1. Deactivate Virtual Environment (Optional): `deactivate`
              ```bash
              (venv) $ deactivate
              $
              ```
     2. **CAT1 Application:** Content-Address Transformation with a CAT:
        1. **[Module Example:](cats/apps/cat1/__init__.py)**: Instantiate `catFactory` within `apps/cat0/__init__.py`
          ```python
          from pycats.factory import Factory
          from pycats.function.infrafunction.plant.spark import SparkSessionConfig
          from pycats import CATS_HOME, SPARK_HOME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

          # Configure Plant Session (Apache Spark Session)
          SparkSessionConfig['spark.app.name'] = 'CAT'
          SparkSessionConfig['spark.executor.instances'] = '4'
          SparkSessionConfig['spark.executor.memory'] = '5g'
          SparkSessionConfig['spark.kubernetes.executor.deleteOnTermination'] = 'true'
          SparkSessionConfig['spark.hadoop.fs.s3a.access.key'] = AWS_ACCESS_KEY_ID
          SparkSessionConfig['spark.hadoop.fs.s3a.secret.key'] = AWS_SECRET_ACCESS_KEY
          SparkSessionConfig['spark.kubernetes.file.upload.path'] = 's3a://cats-storage/input/'
          SparkSessionConfig['spark.pyspark.driver.python'] = f'{CATS_HOME}/venv/bin/python'

          CAT_APP_HOME = f"{CATS_HOME}/apps/cat1/cat.py"
          TRANSFORM_SOURCE = f"{CATS_HOME}/apps/cat1/transform.py"
          TRANSFORM_DEST = 's3://cats-public/cad-store/cad/transformation/transform.py'
          tf_script = f'{CATS_HOME}/cluster/tf_cluster_setup.sh'
          tf_cmd = f"bash {tf_script}"
          catFactory = Factory(
              plantConfig=SparkSessionConfig, # Configuration of Plant Session
              DRIVER_IPFS_DIR=f'{CATS_HOME}/catStore', # Local / Node CAT storage
              terraform_cmd=tf_cmd, # Bash script to Terraform Plant Cluster (Kubernetes Pod Group)
              terraform_file=f'{CATS_HOME}/main.tf', # Terraform file to CID for catBOM
              SPARK_HOME=SPARK_HOME, # Plant Home Environmental Variable
              CAT_APP_HOME=CAT_APP_HOME, # Plant Application
              TRANSFORM_SOURCE=TRANSFORM_SOURCE, # Local / Node data transformation module for CAT
              TRANSFORM_DEST=TRANSFORM_DEST # Cluster file system URI data transformation module for CAT will be written to
          )
          ```
        2. Content-Address Transform CAI into CAO with CAT `Processor` produced by `catFactory` within `apps/cat1/cat.py`
             1. Process Input
                * **input_bom_path** - URI of Input BOM
                * **cao_partitions** - Partition count of an Invoice/CAD representing the amount of concurrent threads used 
                to generate it
                * **input_bom_update** - Updates the input BOM key-value pairs from another CAT
                  * **cao_data_uri** - URI to transfer data from IPFS to cluster file system for processing
                * Process Output URIs as Input
                   * **cat_log_path** - contains IPFS client, IaC (terraform) address, and the transformation process address
                   * **output_bom_path** - URI of Output BOM
                   * **output_bom_update** - Updates the output BOM key-value pairs of current CAT
                     * **cai_data_uri** - Subsequent CAT CAI data URI
                     * **cai_invoice_uri** - Subsequent CAT Invoice/CAI URI
                     * **transform_sourcefile** - Subsequent CAT Source URI of data transformation (Python / Spark SQL)  
                     * **transformer_uri** - Cluster File System URI of subsequent CAT data transformation
                     (**[Data Transformation Example](cats/catStore/cats-public/cad-store/cad/transformation/transform2b.py)**)
             2. **[Module Example:](cats/apps/cat1/cat.py)**
             ```python
             from apps.cat1 import catFactory
             from pycats import CATSTORE
             from pycats.function.process.cat import Processor

             cat: Processor = catFactory.init_processor().get_driver_ipfs_id()
             cat.transform(
                 input_bom_path='s3://cats-public/cad-store/cad/cai/bom/bom.json',
                 output_bom_path='s3://cats-public/cad-store/cad/cao/bom/output_bom.json',
                 cat_log_path='/tmp/bom_cat_log.json',
                 cao_partitions=1,
                 input_bom_update={
                     'cao_data_uri': 's3://cats-public/cad-store/cad/cao/data'
                 },
                 output_bom_update={
                     'cai_data_uri': 's3://cats-public/cad-store/cad/cai2/data',
                     'cai_invoice_uri': 's3://cats-public/cad-store/cad/cai2/invoices',
                     'transform_sourcefile': f'{CATSTORE}/cad/transformation/transform2b.py',
                     'transformer_uri': 's3://cats-public/cad-store/cad/transformation/transform2b.py'
                 }
             )
             ```
     3. **CAT1 Process Output:**
        ```bash
        # Output Dataset that has been Content-Addressed (See Invoice / CAD for CAT1)
        +-----------+-------+-------+-------+-------+-------+
        |row_sum_sum|_c0_sum|_c1_sum|_c2_sum|_c3_sum|_c4_sum|
        +-----------+-------+-------+-------+-------+-------+
        |    25395.0| 5070.0| 5340.0| 5570.0| 5180.0| 4235.0|
        |    20482.0| 3990.0| 4178.0| 4608.0| 4085.0| 3621.0|
        +-----------+-------+-------+-------+-------+-------+

        # CAO BOM
        {'action': 'added',
        'bom_cid': 'QmasVxwJNMN1WdDpYGFyZggnMpnZLMPSQ2dnr45bKhG6gh',
        'cad_bom_uri': 's3://cats-public/cad-store/cad/cao/bom/output_bom.json',
        'cad_cid': 'QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH',
        'cai_data_uri': 's3://cats-public/cad-store/cad/cai2/data',
        'cai_invoice_uri': 's3://cats-public/cad-store/cad/cai2/invoices',
        'cao_data_uri': '',
        'cao_part_cids': ['QmfE66332BexNKENyV9wgRbHbmZDRnqhj5bv6gpEKc8iUm'],
        'input_bom_cid': 'QmQaYFQ9naBFSTthjiyFLPfu8CnVNf6c2Ju9PbyhyZLqmb',
        'invoice_cid': '',
        'log_write_path_uri': 's3://cats-public/cad-store/cad/cao/bom/bom_cat_log.json',
        'transform_cid': 'QmWEqWrgGqsej9xxb2Z1ctm7LNH6GKYFgeXcwFG2nYFVtD',
        'transform_filename': 'transform2b.py',
        'transform_node_path': '/opt/spark/work-dir/job/transformation/transform2b.py',
        'transform_sourcefile': '/home/jjodesty/Projects/Research/cats/apps/cat1/transform2b.py',
        'transform_uri': 's3://cats-public/cad-store/cad/transformation/transform2b.py',
        'transformer_uri': 's3://cats-public/cad-store/cad/transformation/transform2b.py'}

        # CAT log: Addresses
        {'addresses': ['/ip4/70.107.79.74/tcp/29347/p2p/12D3KooWNZ9C3mHTwZMYwnwcYWn8wbEkNRRFS4Ze27QnuK1jAB1R',
                       '/ip4/172.17.0.3/tcp/4001/p2p/12D3KooWNZ9C3mHTwZMYwnwcYWn8wbEkNRRFS4Ze27QnuK1jAB1R'],
         'terraform_addresses': ['/ip4/192.168.1.27/tcp/4001/p2p/12D3KooWMqjgHjaxpHqQUuBrzPJS7nM1QLQ2tTHZoLYEVVqEbdyD',
                                 '/ip4/70.107.79.74/tcp/38211/p2p/12D3KooWMqjgHjaxpHqQUuBrzPJS7nM1QLQ2tTHZoLYEVVqEbdyD'],
         'transformer_addresses': ['/ip4/172.17.0.4/tcp/4001/p2p/12D3KooWPuCynRm1Xm1tTxzcQatwHjajNteTPdcczU7h1EG2osyG',
                                   '/ip4/70.107.79.74/tcp/26037/p2p/12D3KooWPuCynRm1Xm1tTxzcQatwHjajNteTPdcczU7h1EG2osyG']} 
        ```