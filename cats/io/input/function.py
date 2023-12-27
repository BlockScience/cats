from pprint import pprint

import ray
from typing import Dict
import numpy as np

from cats.service import Service


class Processor:
    def __init__(self, service: Service):
        self.service = service
        self.processCID = self.service.processCID
        self.process = self.service.process
        self.inDataCID = self.service.enhanced_bom['init_data_cid']
        # self.inDataCID = self.service.enhanced_bom['invoice']['data_cid']
        self.outDataCID = None
        self.seedCID = None

        self.ingress_job_id = None
        self.ingress_s3_input = None
        self.integration_s3_output = None
        # self.integration_job_id = None
        self.egress_job_id = None

    def Ingress(self):
        # print(self.inDataCID)
        # exit()
        self.ingress_job_id = self.service.meshClient.ingress(input=self.inDataCID)
        self.service.meshClient.checkStatusOfJob(job_id=self.ingress_job_id)
        return self.ingress_job_id

    def Integration(self):
        self.ingress_s3_input = self.service.meshClient.integrate(job_id=self.ingress_job_id)
        self.integration_s3_output = "s3://" + self.ingress_s3_input.split('//')[-1].rsplit('/outputs/')[0] + "-integrated"
        # s3://catstore3/boms/result-20231220-1cc866b0-9b40-48d0-879d-f00684ac89ae/outputs/
        # print(self.ingress_s3_input)
        # print(self.integration_s3_output)
        # exit()
        ds = ray.data.read_csv(self.ingress_s3_input)
        transformed_ds = ds.map_batches(self.process)
        print(transformed_ds.show(limit=1))
        transformed_ds.write_csv(self.integration_s3_output)
        return self.integration_s3_output

    def Egress(self):
        self.egress_job_id = self.service.meshClient.egress(integration_s3_output=self.integration_s3_output)
        self.service.meshClient.checkStatusOfJob(job_id=self.egress_job_id)
        return self.egress_job_id

    def execute(self):
        self.ingress_job_id = self.Ingress()
        self.integration_s3_output = self.Integration()
        self.egress_job_id = self.Egress()
        return self.ingress_job_id, self.integration_s3_output, self.egress_job_id


class InfraFunction(Processor):
    def __init__(self, service: Service):
        self.service = service
        # self.infrafunctionCID = self.service.infrafunctionCID
        self.process: Processor = Processor(self.service)


class Function(InfraFunction):
    def __init__(self, service: Service):
        self.service: Service = service
        self.infraFunction: InfraFunction = InfraFunction(self.service)
        self.processor: Processor = self.infraFunction.process
        self.process = self.service.process
        self.ingress_job_id = None
        self.integration_s3_output = None
        self.egress_job_id = None

    def execute(self):
        self.ingress_job_id, self.integration_s3_output, self.egress_job_id = self.processor.execute()
        return self.ingress_job_id, self.integration_s3_output, self.egress_job_id