# CATs: Content-Addressable Transformers

### What CATs do:
CATs is unified processing software framework and web application back-end that enables the creation of Web3 decentralized 
data products with data process verification using Web2 centralized cloud services (SaaS, PaaS, IaaS), collaboration 
across domains between cross-functional teams and organizations on products by 
[**Content-Addressing**](https://en.wikipedia.org/wiki/Content-addressable_storage) the means of processing and using 
Content-Addresses as the means of dataset transport between processes.

### Illustrated CAT:
![alt_text](https://github.com/BlockScience/cats/blob/local_fs/images/simple_cat_9.jpeg?raw=true)

### Why CATs are useful:
* **Execution:**
  * CATs execute Distributed Processes which are distributed as tasks for Concurrent and/or Parallelized execution on Web2 
    infrastructure
* **Data Verification:**
  * Content-Addresses can be used to verify data processing (input, transformation / process, output, infrastructure)
    * Enables data process re-execution via retrieval of said means using IPFS CIDs as Content-Addresses
* **Data & Process Lineage & Provenance:**
  * Certifies the accuracy of data processing on data products and pipelines by enabling maintenance & reporting of data 
  and process lineage & provenance as chains of evidence
* **Collaboration:**
  * Cross-functional teams & organization for collaboration across domains on verifiable data processes via a UI that 
  accepts Data Provenance record entry as Input that is also CAT Output
  
### Content-Addressing Data Processing with [IPFS](https://ipfs.io/):
* IPFS **[CIDs](https://docs.ipfs.io/concepts/content-addressing/)** (Content Identifiers) are used as content addresses 
that provide the means of verifying data transformation accuracy.
* IPFS **[client](https://docs.ipfs.io/install/command-line/#official-distributions)** is used to identify and retrieve 
inputs, transformations, and outputs for verifying transformation accuracy given CIDs

### Design:
**CATnode Architectural Quantum:** Domain Agnostic Data Product Collaboration
    
   * **Network Planes:**
        * **Action Plane:** Web2 Data Plane exposed to a Web3 Data Plane
            * Content-Addressed communication between services
        * **Control Plane:**
            * Management of the configuration and policies of Web3 communication
   * **Properties:**
        * Maintains separation Mechanisms (Action) & Policies (Control)
   * **Control:** Asynchronous Inter-Process Communication with Action from Actor
   * **Components:**
       * **Structure:**
           * **Plant (Software as a Service \[SaaS\])** - User specified computational / data transformation framework / 
           software (Spark / Dask / etc.)
           * InfraStructure - CAT infrastructure as code (IaC)
       * **Function:**
           * **Process** - Data Transformation UI / Computational Process performed by Plant (SQL, DataFrame, …)
           * **InfraFunction** - Plant interface for running Processes
         
**CATnode Component Based Diagram:** a Web3 p2p mesh client used to create and connect a Web2 cloud service to a 
Decentralized Service Mesh network
   * **Input:**
       * Function as code (Process)
       * Input Data
       * \[Infra\]Structure as Code (IaC)
   * **CAT**
       * **CAT Factory** constructs Function and Structure
       * Function executes on Structure to produce output data
        

### CAT Concepts:
CATs (Data) Pipeline inputs (I/O Data & Transformations) produce a sequence of Bill of Content Addressed Materials 
(catBOM) that enable Data Provenance and cross-organization participation on (big) data processing using Distributed 
(Data) Processing frameworks
* **Fundamental:**
  * **Data Provenance** - a means of proving data lineage using historical records that provide the means of pipeline 
  re-execution and data validation.
  * **Bill of Materials (BOM)** - an extensive list of raw materials, components, and instructions required to 
  construct, manufacture, or repair a product or service.
  * **Distributed (Data) Processing** - typically concurrently parallel (data) processes distributed to networked computers
* **CATs Data Provenance as CAT I/O (a.k.a catBOM as Provenance Record):**
    * **catBOM** - a collection of CIDs & URIs metadata for establishing provenance that enable (re-)execution of CAT processes
        * catBOM values are modifiable I/O for CATs
        * CIDs are used to retrieve CAT Input off IPFS and transfer them between CATs & on separate on CATclusters
        * URIs identify CATclusters’ Distributed File System (FS) used as Distributed DataFrame transformation cache 
        of a Content Addressed Dataset (CAD)
        * Current & Input BOM CIDs & BOM I/O URIs
        * **CAT I/O within catBOM**
          * **Invoice / Content-Addressed Dataset (CAD)** - a collection IPFS CIDs of Data Partitions and their partition 
          URIs. Partitions are generated by CAT DataFrame Partition Shuffling across Worker Nodes of CATclusters
              * Invoice URI (contains CAT I/O)
          * **Transformer URI & CID** (CAT Object Configuration & CAT input)
              * Transformer URIs (of DataFrame Transformation cache)
          * **Content-Addressed Input (CAI)** URI & CIDs - an input Dataset for a CAT that has been content-addressed
          * **Content-Addressed Output (CAO)** URI & CIDs - an output Dataset of a CAT that has been content-addressed
    * **BOMchain** - Linked List of catBOMs used to create & execute CATpipes (Data Pipelines of CATs)
      * CATpipe I/O
      * Can be used for data pipeline verification

### Next Steps:
1. Replace s3 with Filebase for Content-Addressable Storage in order to remove ipfs client from cluster workers
2. Integration Tests
3. Implement CATnode:

    A.Options:
      * CATsVM Disk Image (Ubuntu)
      * CATsContainer using docker:latest container (Alpine Linux)

    B. Add dependencies to Terraform one CATnode exists
4. Unit Tests
5. Produce new SaaS Plants with CAT Factory

### Long-Term Vision:
  * CATs are intended to be executed on a peer-to-peer (p2p) mesh network client
  * CATs is intended to enable the offering of Web2 cloud services (SaaS, PaaS, IaaS) as Web3 peers / smart contracts 
  by Content-Addressing the entire Cloud Service Model for such services

### [Installation](Installation.md)

### [Usage](USAGE.md)


**Image Citations:**
* **["Illustrated CAT"](https://github.com/BlockScience/cats#illustrated-cat)**
  * [Python logo](https://tse4.mm.bing.net/th?id=OIP.ubux1yLT726_fVc3A7WSXgHaHa&pid=Api)
  * [SQL logo](https://cdn3.iconfinder.com/data/icons/dompicon-glyph-file-format-2/256/file-sql-format-type-128.png)
  * [Terraform logo](https://tse2.mm.bing.net/th?id=OIP.1gAEVon2RF5oko4iWCfftgHaHO&pid=Api)
  * [IPFS logo](https://tse1.mm.bing.net/th?id=OIP.BRyW5Tdm5_6VQxCsGr_sQAHaHa&pid=Api)
  * [cat image](https://tse1.mm.bing.net/th?id=OIP.xS_itpeyTImMcrcQ_YNsfQHaIu&pid=Api)
  * [Apache Spark logo](https://tse1.mm.bing.net/th?id=OIP.3qXr4urfJiEWj_fcXhZs-AHaD2&pid=Api)