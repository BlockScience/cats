# from cats.io.input.structure import Structure
# from cats.io.input.function import Function
# from cats.io.input.order import Order
# from cats.io.output import Invoice
import json
import os
import pickle
from pprint import pprint

from cats.io.input.structure import Structure
from cats.io.input.function import Function
from cats.service import Service


class Executor(Structure):
    def __init__(self,
        service: Service
    ):
        self.service: Service = service
        self.structure: Structure = Structure(self.service)
        self.function: Function = Function(self.service)
        self.bom_json_cid: str = self.service.bom_json_cid
        self.enhanced_bom, self.bom = self.service.meshClient.getEnhancedBom(self.bom_json_cid)
        self.orderCID = None
        self.invoiceCID = None

        self.ingress_job_id = None
        self.integration_s3_output = None
        self.egress_job_id = None

        # self.order = None
        # self.structure: Structure = self.order.structure
        # self.function: Function = self.order.function
        # ...

    # def execute(self):
    #     self.invoiceCID = self.enhanced_bom['invoice_cid']
    #     self.orderCID = self.enhanced_bom['invoice']['order_cid']
    #     self.structure.deploy()
    #     self.ingress_job_id, self.integration_s3_output, self.egress_job_id = self.function.execute()
    #     self.enhanced_bom['function'] = json.loads(
    #         self.service.meshClient.cat(self.enhanced_bom['order']['function_cid'])
    #     )
    #     self.enhanced_bom['log'] = {
    #         'ingress_job_id': self.ingress_job_id,
    #         'integration_s3_output': self.integration_s3_output,
    #         'egress_job_id': self.egress_job_id
    #     }
    #     self.enhanced_bom['invoice']['data_cid'] = self.service.meshClient.getEgressOutput(job_id=self.egress_job_id)
    #     self.enhanced_bom['log_cid'] = self.service.ipfsClient.add_json(self.enhanced_bom['log'])
    #     return self.enhanced_bom, None

    def execute(self, enhanced_bom=None):
        if enhanced_bom is not None:
            self.enhanced_bom = enhanced_bom

        self.invoiceCID = self.enhanced_bom['invoice_cid']
        self.orderCID = self.enhanced_bom['invoice']['order_cid']

        self.structure.deploy()
        self.ingress_job_id, self.integration_s3_output, self.egress_job_id = self.function.execute()
        self.enhanced_bom['function'] = json.loads(self.service.meshClient.cat(self.enhanced_bom['order']['function_cid']))
        self.enhanced_bom['log'] = {
            'ingress_job_id': self.ingress_job_id,
            'integration_s3_output': self.integration_s3_output,
            'egress_job_id': self.egress_job_id
        }
        self.enhanced_bom['invoice']['data_cid'] = self.service.meshClient.getEgressOutput(job_id=self.egress_job_id)
        self.enhanced_bom['log_cid'] = self.service.ipfsClient.add_json(self.enhanced_bom['log'])

        del self.enhanced_bom['bom_json_cid']
        del self.enhanced_bom['init_data_cid']
        os.remove("bom.json")
        os.remove("invoice.json")
        os.remove("order.json")
        os.remove("bom.car")
        os.remove("cat-action-plane-config")
        return self.enhanced_bom, None
        # return self.invoiceCID

    # def deploy(self, function: Function):
    #     self.exe_response = function.deploy()
    #     return self.exe_response
