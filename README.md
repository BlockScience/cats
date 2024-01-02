# CATs: Content-Addressable Transformers
![alt_text](images/CATs_chaordic_kernel.jpeg)


**Content-Addressable Transformers** (**CATS**) is a unified data service collaboration framework that establishes a scalable and 
self-serviced Data Platform as a Data Mesh network of scalable & distributed computing workloads with Data Provenance. 
CATs uses interoperable distributed computing frameworks deployable on Kubernetes.

### Data Service collaboration via CATs:
CAT Mesh streamline data service collaboration between organizations by providing a reliable and efficient way to manage, 
share, and reference data and data processing by Content-Addressing the means of data transformation. **Content-Addressing** is a method of uniquely identifying and retrieving data based on its content rather than its location 
or address. 

##### Collaborative Value of CATs:
* Organizations participating in Strategic Partnerships will employ CATs for rapid ratification of service agreements 
within collaborative feedback loops of Data Initiatives
* CATs will be compiled and executed as interconnecting services on a Data Mesh that grows naturally when organizations 
communicate CATs provenance records (a.k.a BOMs (Bills of Materials)) within feedback loops of Data Initiatives

![alt_text](images/CATs_bom_ag.jpeg)

### CAT Mesh: ***CATs' self-serviced Data Mesh platform***

CATs establishes a scalable and self-serviced Data Mesh platform (**CAT Mesh**) for Multi-disciplinary and 
cross-fuctional teams to verify and scale distributed computing workloads with Data Provenance using interoperable 
computing frameworks deployable on **[Kubernetes](https://kubernetes.io/)** for Big Data processing with Scientific 
Computing capabilities.

**Value:**

CAT Mesh enables workloads to be portable between Web2 & Web3 infrastructure with minimal rework or modification. This portability closes 
the gap between data analysis and business operations by connecting Web3 and Web2 network planes. 

**Means: Content-Addressing**

CAT Mesh workloads (or CATs) interface cloud service model (SaaS, PaaS, IaaS) offered by providers such as AWS, GCP, Azure, etc. on a 
Mesh Network interconnected by [**Content-Addresed**](https://en.wikipedia.org/wiki/Content-addressable_storage) 
data transport solutions such as [IPFS](https://ipfs.io/).
* IPFS **[CIDs](https://docs.ipfs.io/concepts/content-addressing/)** (Content-Identifiers) are used as content addresses 
that provide the means of verifying data transformation accuracy.
* IPFS **[client](https://docs.ipfs.io/install/command-line/#official-distributions)** is used to identify and retrieve 
inputs, transformations, outputs, and infrastructure (as code [IaC]) for verifying transformation accuracy given CIDs

![alt_text](images/cid_example.jpeg)

### CATs' Data Provenance Record: Bill of Materials
**BOM (Bill of Materials):** 
CATs Content-Addressed Data Provenance record for verifiable data processing and transport on 
a Mesh network of CATs. BOMs are used as CAT’ input & output that contain CATs’ means of data processing

![alt_text](images/CATs_bom_activity.jpeg)

BOMs employ CIDs for location-agnostic retrieval based on its content as well as processes and 
[Data Veification](https://en.wikipedia.org/wiki/Data_verification). BOM CIDs can be used to verify the means of processing 
data (input, transformation / process, output, infrastructure-as-code (IaC)). they can also 
make CATs resilient by enabling re-execution via retrieval. CATs certifies the accuracy of data processing on data 
products and pipelines by enabling maintenance & reporting of 
[data and process lineage & provenance](https://bi-insider.com/posts/data-lineage-and-data-provenance/) as chains of 
evidence using CIDs.

**Interconnect CATs:** ***Establish a CAT Mesh with Data Provenance***

CAT Mesh is composed by CATs executing BOMs.

![alt_text](images/CATs_bom_connect.jpeg)

### Get Started!
##### A. Installation:
0. **[Python](https://www.python.org/downloads/)** (>= 3.10.13)
1. **[kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installing-from-release-binaries)** (>= 0.12.0)
2. **[kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)** (>= 1.22.2)
3. **[helm](https://helm.sh/docs/intro/install/)** (>= v3.13.1)
4. **[CoD](https://docs.bacalhau.org/getting-started/installation/)** (>= v1.2.0)
   ```bash
   curl -sL https://get.bacalhau.org/install.sh | bash
   ```
5. **[Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)** (>= 1.5.2)
6. **[IPFS Kubo](https://docs.ipfs.tech/install/command-line/#system-requirements)** (0.24.0)
7. **[AWS S3](https://aws.amazon.com/s3/)**
8. **Install CATs**
    ```bash
    git clone ...
    ```
#####  B. [Prepare CAT Node's Execution Environment](./docs/ENV.md)
#####  C. Deploy CAT Node:
  ```bash
  cd <CATs parent directory>/cats-research
  source ./venv/bin/activate
  # (venv) $
  PYTHONPATH=./ python catMesh/cat/node.py
  ```
#####  C. [Establish CAT Mesh](./cats_demo.ipynb)


### Orginizational Value:
CATs empower effective cross-domain collaboration on a 
[**Data Mesh of Data Products**](https://martinfowler.com/articles/data-mesh-principles.html) across business and 
knowledge domains between cross-functional & multi-disciplinary teams and organizations. A Data Mesh solution involves 
Data Products implemented, operated, and maintained by multidisciplinary teams on a self-service Data Mesh platform. 
Data Products service each other as well as end users on this platform. The Data Mesh solution is accomplished by 
federated governance of Data Products and Domains served on a Data Mesh. Individual Data Products and their 
infrastructure are owned and operated by multidisciplinary teams. This is a customer-centric approach to 
overall project implementation life-cycles with nested Data Product life-cycles that have tighter loops (a.k.a. 
Agility).
The advantages of principles and architecture include the following:
    
* **Operational Value:**
    * Reduced operational bottlenecks caused by the communication overheads of cross-team/departmental synchronization 
    * between siloed groups such as cross-disciplinary miscommunication. These overheads are associated with the 
    * coordination of siloed groups constituted of different roles within organizations.
    * Increased service and product agility with the employment of multi-disciplinary teams that operate, maintain, and 
    * potentially own their own infrastructure because there is less infrastructure to own
    * Reduced the operational overhead of data discovery by Content-Addressing the means of processing (input and output 
 data, transformation / process, and infrastructure [as Code (IaC)] and using Content-Addresses as the means of data 
 transport between services.
    * “Improving data quality and resilience of analysis (BI, AI) by bringing producers closer to consumers (removing 
the complexity of intermediate data pipelines)” ([1.](https://en.blog.businessdecision.com/data-domains-data-mesh-gives-business-domains-superpowers/))

* **Business Value:**
    * Enables more control over their data, agility for market reactivity and business scope changes, and data quality increases due to a self-service Data Mesh platform that enables federated governance and increased project visibility ([1.](https://en.blog.businessdecision.com/data-mesh-ultimate-model-for-data-driven-companies/))
    * Enables rational expense estimates of operational and maintenance per data domain ([2.](https://en.blog.businessdecision.com/data-infrastructure-self-service-data-mesh/))
    * Enables Data Services to grow with and adapt to changes to the organization and/or business ([1.](https://en.blog.businessdecision.com/data-domains-data-mesh-gives-business-domains-superpowers/))

### CATs Architectural Quantum (Domain-Driven Design principle):
![alt_text](images/CATkernel.jpeg?raw=true)
CAT’s architectural design and implementation are the result of applied Engineering, Computer Science, Network Science, 
and Social Science. CATs is software executing on a network client ontological to an MicroKernel Operating System. CATs’ 
is designed to enable Data Products implemented as compute node peers on a Data Mesh network that encapsulate code, 
data, metadata, and infrastructure to function as a service providing access to the business domain's analytical data as 
a product. Data Products use the Architectural Quantum domain-driven design principle for peer nodes that represent the 
“smallest unit of architecture that can be independently deployed with high functional cohesion, and includes all the 
structural elements required for its function” 
([“Data Mesh Principles and Logical Architecture”](https://martinfowler.com/articles/data-mesh-principles.html#:~:text=smallest%20unit%20of%20architecture%20that%20can%20be%20independently%20deployed%20with%20high%20functional%20cohesion%2C%20and%20includes%20all%20the%20structural%20elements%20required%20for%20its%20function.) - Zhamak Dehghani, et al.).

### Collaborative value of CATs Architectural Quantum:
The operation and maintenance of CATs’ Data Products on a Data Mesh can occur between independent teams that will operate, contribute, and maintain different portions of the entire cloud-service model in adherance to CATs' Architectural Quantum in a way suitable for their roles using the CATs’ API to serve individual Data Model entities on a Data Mesh for a variety of use-cases. CAT’s Data Product teams can be multidisciplinary due to the fact they can operate and maintain the different portions of the entire Web2 cloud service model based on role. 
For example:
* An **Analyst** or **Data Scientist** will use CATs Process interface deployed as SaaS for Analytical Data transformation
* A **Backend** or **ML-Engineer** implementing a CAT application as SaaS for a Data Scientist to execute machine learning models / pipelines on a cloud managed Kubernetes PaaS as opposed to a machine learning handoff deployment.
* An **Infrastructure Engineer** would use the Terraform CDK interface deployed as multi-cloud IaaS for a CAT to be deployed by the Backend or ML-Engineer

### CAT Concepts:
CATs (Data) Pipeline inputs (I/O Data & Transformations) produce a sequence of Bill of Content Addressed Materials 
(catBOM) that enable Data Provenance and cross-organization participation on (big) data processing using Distributed 
(Data) Processing frameworks
* **Fundamental:**
  * **[Data Verification](https://en.wikipedia.org/wiki/Data_verification)** - a process for which data is checked for 
  accuracy and inconsistencies before processed
  * **[Data Provenance](https://bi-insider.com/posts/data-lineage-and-data-provenance/)** - a means of proving data lineage using historical records that provide the means 
  of pipeline re-execution and **[data validation](https://en.wikipedia.org/wiki/Data_validation)**
  * **[Data Lineage](https://bi-insider.com/posts/data-lineage-and-data-provenance/)** - reporting of data lifecyle from source to destination
  * **[Distributed Computing](https://en.wikipedia.org/wiki/Distributed_computing)** - typically the concurrent and/or 
  parallel execution of job tasks distributed to networked computers processing data
  * **[Bill of Materials (BOM)](https://en.wikipedia.org/wiki/Bill_of_materials)** - an extensive list of raw materials,
  components, and instructions required to construct, manufacture, or repair a product or service

### Image Citations:
* **["Illustrated CAT"](https://github.com/BlockScience/cats#illustrated-cat)**
  * [Python logo](https://tse4.mm.bing.net/th?id=OIP.ubux1yLT726_fVc3A7WSXgHaHa&pid=Api)
  * [SQL logo](https://cdn3.iconfinder.com/data/icons/dompicon-glyph-file-format-2/256/file-sql-format-type-128.png)
  * [Terraform logo](https://tse2.mm.bing.net/th?id=OIP.1gAEVon2RF5oko4iWCfftgHaHO&pid=Api)
  * [IPFS logo](https://tse1.mm.bing.net/th?id=OIP.BRyW5Tdm5_6VQxCsGr_sQAHaHa&pid=Api)
  * [cat image](https://tse1.mm.bing.net/th?id=OIP.xS_itpeyTImMcrcQ_YNsfQHaIu&pid=Api)
  * [ray.io logo](https://open-datastudio.io/_images/ray-logo.png)
  
