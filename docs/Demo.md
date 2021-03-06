# Basic Pipeline of CATs (catPipe): Demo Example & Infrastructure

## catPipe Description

This is an example of a catPipe given that the data is not Content-Addressed / initially on the IPFS network. 
This pipeline involves two CAT processes on two separate Apache Spark clusters on the Data Plane of the same Kubernetes 
(K8s) cluster

#### catPipe: CAT Pipeline Activity Diagrams
* catPipe I/O surface is the catBOM above
* catPipe is below

![alt_text](https://github.com/BlockScience/cats/blob/main/images/catPipe.jpeg?raw=true)

## catPipe Infrastructure

#### Initial Infrastructure: 
![alt_text](https://github.com/BlockScience/cats/blob/main/images/cat_demo_infrastructure.jpeg?raw=true)

#### CAT0: Content-Addresses Dataset
* **[CAT0 Demo Example](CAT0-CAD.md)**
* **Updated Infrastructure:**
![alt_text](https://github.com/BlockScience/cats/blob/main/images/cat0_infrastructure_step.jpeg?raw=true)

#### CAT1 Updated Infrastructure: Content-Address Transform
* **[CAT1 Demo Example](CAT1-CAT.md)**
* **Updated Infrastructure:**
![alt_text](https://github.com/BlockScience/cats/blob/main/images/cat1_infrastructure_step.jpeg?raw=true)

### Image Citations: 
* **["catPipe Infrastructure" Images](https://github.com/BlockScience/cats/blob/main/docs/Demo.md#catpipe-infrastructure)**
  * [Minikube logo](https://tse2.mm.bing.net/th?id=OIP.fMjeHmaGDI5UIzzvyDuUoQHaHL&pid=Api)
  * [Kubectl logo](https://tse3.mm.bing.net/th?id=OIP.vEBONA7sJh1FqEJKoR7gMwAAAA&pid=Api)
  * [Apache Spark logo](https://tse1.mm.bing.net/th?id=OIP.3qXr4urfJiEWj_fcXhZs-AHaD2&pid=Api)
  * [PySpark logo](https://tse2.mm.bing.net/th?id=OIP.jLX-o1B65-jzFluLvjMn9wAAAA&pid=Api)
  * [IPFS logo](https://tse1.mm.bing.net/th?id=OIP.BRyW5Tdm5_6VQxCsGr_sQAHaHa&pid=Api)