# Basic Pipeline of CATs (catPipe): Demo Example & Infrastructure

## catPipe Description

This is an example of a catPipe given that the data is not initially on the IPFS network. This pipeline involves 2 
CAT processes on 2 separate Apache Spark clusters on the Data Plane of the same Kubernetes (K8s) cluster

#### catPipe: CAT Pipeline Activity Diagrams
* catPipe I/O surface is the catBOM above
* catPipe is below

![alt_text](https://github.com/BlockScience/cats/blob/main/images/catPipe.jpeg?raw=true)

## catPipe Infrastructure

#### Initial Infrastructure: 
![alt_text](https://github.com/BlockScience/cats/blob/main/images/cat_demo_infrastructure.jpeg?raw=true)

#### CAT0: Content-Addresses Dataset
* **[CAT0 Demo Example](docs/CAT0-CAD.md)**
* **Updated Infrastructure:**
![alt_text](https://github.com/BlockScience/cats/blob/main/images/cat0_infrastructure_step.jpeg?raw=true)

#### CAT1 Updated Infrastructure: Content-Address Transform
* **[CAT1 Demo Example](docs/CAT1-CAT.md)**
* **Updated Infrastructure:**
![alt_text](https://github.com/BlockScience/cats/blob/main/images/cat1_infrastructure_step.jpeg?raw=true)