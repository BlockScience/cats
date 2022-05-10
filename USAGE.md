# Usage: Basic CATpipe (Pipeline of CATs)

#### Description

This is an example of a CAT pipeline given that the data is not initially on the IPFS network. This pipeline involves 2 
CAT processes on 2 separate Apache Spark clusters on the Data Plane of the same Kubernetes cluster

<CAT I/O BOMchain & Surface Images>

**Steps:**
1. Open 2 terminal sessions
2. **CAT0:** 
   * **Description:**
     * CAT0 Content-Addresses Dataset and constructs initial catBOM used by the CAT 1 as form of input
       * CAT0 generates a catBOM by Content Identifying (CIDing) an Invoice of Data Partition Transactions, a Data 
       Transformation, and itself
       * CAT0 decentralizes data by CIDing with IPFS from a centralized source AWS s3
   1. **Execution: terminal session A**
       ```bash
       python apps/cat0/execute.py
       ```
   2. **Module:**
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
         2. **CAT Process Output: Processor**
            * 
3. **CAT1: terminal session B** Content-Address Transform Dataset given CAT0 BOM
   * CAT1 represents 0 to n CATs, is the primary data transformation UI for a CAT, and illustrates a CATpipe
     * CATs uses the catBOM as input and output enabling users to reproduce I/O data using a Content Identified (CIDed) 
     Invoice containing Data Partition Transactions and a CIDed Data Transformation 
       * These transactions are records of data partition add or get command executions of an IPFS client that provide 
       access to Output Data and Transformations generating via CIDs to be accessed on the IPFS p2p network
         * It can also provide access via s3 URIs 
   * 
      1. **Execution:**
       ```bash
       python apps/cat1/execute.py
       ```