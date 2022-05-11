# Usage: Basic CATpipe (Pipeline of CATs)

#### Description

This is an example of a CAT pipeline given that the data is not initially on the IPFS network. This pipeline involves 2 
CAT processes on 2 separate Apache Spark clusters on the Data Plane of the same Kubernetes (K8s) cluster

<CAT I/O BOMchain & Surface Images>

### Illustrated CAT:
![alt_text](https://github.com/BlockScience/cats/blob/local_fs/images/BOMchain_io_surfaces.jpeg?raw=true)

**Steps:**
1. Open 2 terminal sessions
2. **CAT0:** terminal session B - CAT0 Content-Addresses Dataset and constructs initial catBOM used by the CAT 1 as form
of input
   * CAT0 generates a catBOM by Content Identifying (CIDing) an Invoice of Data Partition Transactions, a Data 
       Transformation, and itself
   * CAT0 decentralizes data by CIDing with IPFS from a centralized source AWS s3
   * **Example:**
     1. **Execution: terminal session A**
         Builds (Optional for development), Terraforms minikube K8s cluster & builds Spark Image, and executes a CAT
         ```bash
         python apps/cat0/execute.py
         ```
     2. **Module: CAT0**
        1. **CAT Process Input: Processor**
           1. Process Input
              * **input_data_uri** - URI of Input data
              * **cai_partitions** - Partition count of an Invoice/CAD representing the amount of concurrent threads used 
              to generate it
              * Process Output URIs as Input
                 1. Invoice / Content-Addressed Dataset (CAD)
                    * **invoice_uri** - URI of Invoice/CAD
                 2. CAT Bill Of Materials (BOM) 
                   * **bom_write_path_uri** - URI of BOM
                   * **output_data_uri** - URI of Output Data for subsequent CAT
                   * **transformer_uri** - URI of transformation for subsequent CAT
           ```python
           from pycats import CATS_HOME
           from apps.cat0 import catFactory
           from pycats.function.process.cat import Processor

           cat: Processor = catFactory.init_processor(ipfs_daemon=True)
           local_bom_write_path = f'{CATS_HOME}/catStore/bom.json',
           cai_bom, input_cad_invoice = cat.content_address_input(
               input_data_uri='s3://cats-public/input/df', # I
               invoice_uri='s3://cats-public/cad-store/cad/cai/invoices', # O
               bom_write_path_uri='s3://cats-public/cad-store/cad/cai/bom/bom.json', # O
               output_data_uri='s3://cats-public/cad-store/cad/cao/data', # I/O
               transformer_uri='s3://cats-public/cad-store/cad/transformation/transform.py', # I/O
               cai_partitions=1
           )
           ```     
           2. **CAT Process Output: Processor**
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
4. **CAT1**: terminal session B - Content-Address Transform Dataset given CAT0 BOM
   * CAT1 **is the primary data transformation UI for a CAT** representing 0 to n CATs and illustrates a CATpipe
     * CATs uses the catBOM as input and output enabling users to reproduce I/O data using a Content Identified (CIDed) 
     Invoice containing Data Partition Transactions and a CIDed Data Transformation 
       * These transactions are records of data partition add or get command executions of an IPFS client that provide 
       access to Output Data and Transformations generating via CIDs to be accessed on the IPFS p2p network
         * It can also provide access via s3 URIs
     * **Example:**
       1. **Execution: : terminal session B**
          Builds (Optional for development), Terraforms minikube K8s cluster & builds Spark Image, and executes a CAT
          ```bash
          python apps/cat1/execute.py
          ```
       2. **Module: CAT1**
          1. **CAT Process Input: Processor**
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
                     * **cai_data_uri** - CAI data URI for subsequent CAT
                     * **cai_invoice_uri** - Invoice/CAI URI for subsequent CAT
                     * **transform_sourcefile** - Node Invoice/CAI path for subsequent CAT
                     * **transformer_uri** - Invoice/CAI URI for subsequent CAT
             ```python
             from apps.cat1 import catFactory
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
                     'transform_sourcefile': '/home/jjodesty/Projects/Research/cats/apps/cat1/transform2b.py',
                     'transformer_uri': 's3://cats-public/cad-store/cad/transformation/transform2b.py'
                 }
             )
             ```
             2. **CAT Process Output: Processor**
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
        
        