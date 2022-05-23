# CATs: Content-Addressable Transformers

### Description:
CATs is a unified distributed processing framework and web application back-end on a Kubernetes cluster to be 
orchestrated on a peer-to-peer mesh network client acting as a cluster head node. CATs enable the creation of Web3 data 
products as decentralized service with data process verification using existing Web2 centralized cloud service technologies 
(SaaS, PaaS, IaaS) in AWS, GCP, Azure, etc., without the need of a smart-contract language. CATs nurture collaboration 
across domains between cross-functional / multi-disciplinary teams and organizations on products by 
[**Content-Addressing**](https://en.wikipedia.org/wiki/Content-addressable_storage) the means of processing (input, 
transformation / process, output, infrastructure \[as Code (IaC)\]) and using Content-Addresses as the means of data 
transport between services.

### Illustrated CAT:
![alt_text](images/simple_cat_10.jpeg?raw=true)

### Why CATs are useful:
* **Execution:**
  * CATs execute Distributed Processes which are distributed as tasks for Concurrent and/or Parallelized execution on Web2 
    infrastructure
* **Data Verification:**
  * Content-Addresses can be used to verify data processing (input, transformation / process, output, infrastructure)
    * Enables data process re-execution via retrieval of said means using IPFS CIDs as Content-Addresses
* **Data (& Process) Lineage & Provenance:**
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

### CAT Concepts:
CATs (Data) Pipeline inputs (I/O Data & Transformations) produce a sequence of Bill of Content Addressed Materials 
(catBOM) that enable Data Provenance and cross-organization participation on (big) data processing using Distributed 
(Data) Processing frameworks
* **Fundamental:**
  * **[Content-Addressable Storage](https://en.wikipedia.org/wiki/Content-addressable_storage)** - a way to store 
  information such that it can be retrieved based on its content rather than its location
  * **[Data Verification](https://en.wikipedia.org/wiki/Data_verification)** - a process for which data is checked for 
  accuracy and inconsistencies before processed
  * **[Data (& Process) Lineage & Provenance](https://bi-insider.com/posts/data-lineage-and-data-provenance/)** 
    * **Data Lineage** - reporting of data lifecyle from source to destination
    * **Data Provenance** - a means of proving data lineage using historical records that provide the means of pipeline 
    re-execution and **[data validation](https://en.wikipedia.org/wiki/Data_validation)**
  * **[Distributed Computing](https://en.wikipedia.org/wiki/Distributed_computing)** - typically the concurrent and/or 
  parallel execution of job tasks distributed to networked computers processing data
  * **[Bill of Materials (BOM)](https://en.wikipedia.org/wiki/Bill_of_materials)** - an extensive list of raw materials,
  components, and instructions required to construct, manufacture, or repair a product or service
  

### CATs Data Provenance as CAT I/O: catBOM as Provenance Record
* **catBOM** - a collection of CIDs & URIs metadata for establishing provenance that enable (re-)execution of CAT 
processes
    * catBOM values are modifiable I/O for CATs
      * CIDs are used to retrieve CAT Input off IPFS and transfer them between CATs & on separate on CATclusters
      * URIs identify CATclusters’ Distributed File System (FS) used as Distributed DataFrame transformation cache 
      of a Content Addressed Dataset (CAD)
      * Current & Input BOM CIDs & BOM I/O URIs
    * **Illustration of catBOM as I/O surface of CAT**
    ![alt_text](images/BOM_only_with_io_surfaces.jpeg?raw=true)
      * **catBOM Contents:**
        * **Invoice / Content-Addressed Dataset (CAD)** - a **data format** Content-Addressed Data generated by IPFS 
        CIDing events as a collection IPFS CIDs of Dataset Partitions and partition URIs. Partitions are generated by 
        CAT DataFrame Partition Shuffling across Worker Nodes of CATclusters
          * **Content-Addressed Input (CAI)** URI & CIDs - an input dataset for a CAT that has been content-addressed
          as an Invoice/CAD
          * **Content-Addressed Output (CAO)** URI & CIDs - an output dataset of a CAT that has been content-addressed
          as an Invoice/CAD
          * Invoice URI (contains CADs as CAT I/O)
        * **Transformer URI & CID** (CAT Object Configuration & CAT input)
          * Transformer URIs (of DataFrame Transformation cache)
* **BOMchain** - Linked List of catBOMs used to create & execute **CATpipes** (Data Pipelines of CATs)
  * BOMchain is modifiable I/O for CATpipe
    * Can be used for data pipeline verification
  * **Illustration of BOMchain as I/O surface of CATpipe**
  ![alt_text](images/BOMchain_only.jpeg?raw=true)
  
### Next Steps:
1. Replace s3 with Filebase for Content-Addressable Storage in order to remove ipfs client from cluster workers
   1. Alternative: for IPFS server bug (`ipfs init --profile server`) - loop IPFS initialization until provided a public 
   IP Address
2. Implement CATnode MVP to remove the need for users to install dependencies:

    A.Options:
      * CATsVM Disk Image (Ubuntu)
      * CATsContainer

    B. Add dependencies to Terraform one CATnode exists
3. Unit Test: BOM CID equivalence
4. Distributed debugger for Plant(s) \[SaaS(s)\]
5. Unit & Integration Tests
6. Produce new SaaS Plants with CAT Factory
7. CI/CD
8. Provenance catBOM
9. Options to Content-Address Everything

### Long-Term Vision:
  * CATs software is on a peer-to-peer (p2p) mesh network client that enable products implemented with the entire Cloud 
  Service Model to be Decentralized Cloud Services as a Smart Contract (DCSaaSM) by Content-Addressing the entire service.
  * **[IPFS Compute](https://pkg.go.dev/github.com/abhiyerra/ipfs-compute)** will be used to as a 
  [WebAssembly](https://webassembly.org/) (WASM) module task server, broadcaster, & executor leveraging 
  [IPFS Lite](https://github.com/hsanjuan/ipfs-lite) on cluster nodes for distributed processing 

### [Installation](docs/Installation.md)

### [Demo Example & Infrastructure](docs/Demo.md)


### Image Citations:
* **["Illustrated CAT"](https://github.com/BlockScience/cats#illustrated-cat)**
  * [Python logo](https://tse4.mm.bing.net/th?id=OIP.ubux1yLT726_fVc3A7WSXgHaHa&pid=Api)
  * [SQL logo](https://cdn3.iconfinder.com/data/icons/dompicon-glyph-file-format-2/256/file-sql-format-type-128.png)
  * [Terraform logo](https://tse2.mm.bing.net/th?id=OIP.1gAEVon2RF5oko4iWCfftgHaHO&pid=Api)
  * [IPFS logo](https://tse1.mm.bing.net/th?id=OIP.BRyW5Tdm5_6VQxCsGr_sQAHaHa&pid=Api)
  * [cat image](https://tse1.mm.bing.net/th?id=OIP.xS_itpeyTImMcrcQ_YNsfQHaIu&pid=Api)
  * [Apache Spark logo](https://tse1.mm.bing.net/th?id=OIP.3qXr4urfJiEWj_fcXhZs-AHaD2&pid=Api)