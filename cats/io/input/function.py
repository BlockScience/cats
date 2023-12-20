from pprint import pprint

import ray
from typing import Dict
import numpy as np

from cats.service import Service


class Processor:
    def __init__(self, service: Service): # ,
        self.service = service
        self.processCID = self.service.processCID
        self.process = self.service.process
        self.inDataCID = self.service.enhanced_bom['invoice']['data_cid']
        self.outDataCID = None
        self.seedCID = None

        # self.ingress_subproc = self.service.get_ingress_subproc()
        # self.integration_subproc = self.service.get_integration_subproc()
        # self.egress_subproc = self.service.get_egress_subproc()

        self.ingress_job_id = None
        self.ingress_s3_input = None
        self.integration_s3_output = None
        # self.integration_job_id = None
        self.egress_job_id = None

    def Ingress(self):
        # self.service.meshClient.submitJob("bafybeifgqjvmzbtz427bne7af5tbndmvniabaex77us6l637gqtb2iwlwq")
        # ingress_cid = self.service.enhanced_bom['order']['ingress_cid']
        # ingress_uri = self.service.meshClient.cat(ingress_cid)
        self.ingress_job_id = self.service.meshClient.ingress(input=self.inDataCID)
        self.service.meshClient.checkStatusOfJob(job_id=self.ingress_job_id)
        return self.ingress_job_id
        # return self.ingress_subproc(self.ingress_op)(self.enhanced_bom['invoice']['data_cid'])

    """
    {'bom_json_cid': 'QmPaT21Q7a7AZ54EJHnrPRRdy1TCE2iFNqhRpB6g1cdXax',
 'invoice': {'data_cid': 'ipfs://QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp:/inputs/data.tar.gz',
             'order_cid': 'QmXC3eM8FvWhv3VJws9b5jbpXBMnAtCrSkwyMu6WEJxhvp',
             'seed_cid': None},
 'invoice_cid': 'QmXgsbgCpKwK5A5WodyB4kf5ajzBi3UFyHGo7YJgfirHEj',
 'job_id': '31d9218b-703a-4799-b812-730bc63dab1d',
 'log_cid': None,
 'order': {'function_cid': 'b',
           'invoice_cid': 'QmbLkxiEWd21qa3VxYV6yNAAgCY9Litn3iDA9aoGnHf8qs',
           'structure_cid': {'Hash': 'QmYyFroE2Nw1BVg3D1MQdeZFrMAn9XWYHgWueMUKaRGops',
                             'Name': 'main.tf',
                             'Size': '3449'}}}

    """

    def Integration(self, process):
        self.process = process
        self.ingress_s3_input = self.service.meshClient.integration(job_id=self.ingress_job_id)
        self.integration_s3_output = "s3://" + self.ingress_s3_input.split('//')[-1].rsplit('/outputs/')[0] + "-ingest"
        # s3://catstore3/boms/result-20231220-1cc866b0-9b40-48d0-879d-f00684ac89ae/outputs/

        # Compute a "petal area" attribute.
        def transform_batch(batch: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
            vec_a = batch["petal length (cm)"]
            vec_b = batch["petal width (cm)"]
            batch["petal area (cm^2)"] = vec_a * vec_b
            return batch

        ds = ray.data.read_csv(self.ingress_s3_input)
        transformed_ds = ds.map_batches(transform_batch)
        # transformed_ds = ds.map_batches(self.process)
        transformed_ds.show(limit=1)
        # exit()

        transformed_ds.write_parquet(self.integration_s3_output)
        return self.integration_s3_output
        # return self.integration_subproc(self.integration_op)(self.ingress_address)

    def Egress(self):
        self.egress_job_id = self.service.meshClient.egress(integration_s3_output=self.integration_s3_output)
        self.service.meshClient.checkStatusOfJob(job_id=self.egress_job_id)
        return self.egress_job_id
        # return self.egress_subproc(self.egress_op)(self.integration_address)

    def execute(self, process):
        # self.ingress_address = self.Ingress()
        self.ingress_job_id = self.Ingress()
        self.integration_s3_output = self.Integration(process=process)
        self.egress_job_id = self.Egress()
        return self.ingress_job_id, self.egress_job_id
        # self.integration_address = self.Integration()
        # self.outDataCID = self.Egress()
        # return self.outDataCID


class InfraFunction(Processor):
    def __init__(self, service: Service): #
        self.service = service
        # self.infrafunctionCID = self.service.infrafunctionCID
        # self.ingress_op = self.service.get_ingress_op()
        # self.integration_op = self.service.get_integration_op()
        # self.egress_op = self.service.get_egress_op()
        self.process: Processor = Processor(self.service)


class Function(InfraFunction):
    def __init__(self, service: Service):
        self.service: Service = service
        self.infraFunction: InfraFunction = InfraFunction(self.service)
        self.processor: Processor = self.infraFunction.process
        self.process = self.service.process
        self.ingress_job_id = None
        self.egress_job_id = None


    def execute(self):
        # enhanced_bom, bom = self.service.meshClient.getEnhancedBom(self.bom_json_cid)
        self.ingress_job_id, self.egress_job_id = self.processor.execute(process=self.process)
        return self.egress_job_id
        # ret_code, stdout, stderr = self.infraStructure.apply(skip_plan=True)
        # self.infraStructure.cmd = self.service.executeCMD.__get__(self.infraStructure, Terraform)
        # return enhanced_bom, bom