from pprint import pprint

from cats.service.utils import executeCMD
from cats.network import ipfsApi
from cats.network import MeshClient


class Service:
    def __init__(self,
        meshClient: MeshClient,
        process
    ):
        self.meshClient: MeshClient = meshClient
        self.ipfsClient: ipfsApi = self.meshClient.ipfsClient
        self.executeCMD = executeCMD

        self.init_bom_json_cid = None
        self.init_bom_car_cid = None
        self.enhanced_init_bom = None
        self.enhanced_bom = None
        # self.enhanced_init_bom = None

        self.ingress_subproc_cid = None
        self.integration_subproc_cid = None
        self.egress_subproc_cid = None

        self.ingress_subproc = None
        self.integration_subproc = None
        self.egress_subproc = None

        self.processCID = None
        self.process = process
        self.dataCID = None

        # # self.order_cid = self.enhanced_bom['order_cid']
        # self.bom_json_cid = self.enhanced_bom['bom_json_cid']
        #
        # # self.process_cid = self.enhanced_bom['order']['function_cid']['process_cid']
        # self.invoice_cid = self.enhanced_bom['invoice_cid']
        # self.data_cid = self.enhanced_bom['invoice']['data_cid']

        # self.ingress_subproc_cid = self.enhanced_bom['order']['function_cid']['process_cid']['ingress_subproc_cid']
        # self.integration_subproc_cid = self.enhanced_bom['order']['function_cid']['process_cid']['integration_subproc_cid']
        # self.egress_subproc_cid = self.enhanced_bom['order']['function_cid']['process_cid']['egress_subproc_cid']

        # self.ingress_op = self.enhanced_bom['order']['function_cid']['process_cid']['ingress_op']
        # self.integration_op = self.enhanced_bom['order']['function_cid']['process_cid']['integration_op']
        # self.egress_op = self.enhanced_bom['order']['function_cid']['process_cid']['egress_op']

    # # ToDo: EP: Init CAT
    # def serve(self, response):
    #     self.executor: Executor = Factory(response.json)
    #     self.executor.execute()
    #
    # # ToDo: EP: CAT
    # def serve(self, response):
    #     self.executor: Executor = Factory(response.json)
    #     self.executor.execute()

    # def get_ingress_subproc(self):
    #     return self.meshClient.get(self.ingress_subproc_cid)

    # def get_integration_subproc(self):
    #     return self.meshClient.get(self.integration_subproc_cid)

    # def get_egress_subproc(self):
    #     return self.meshClient.get(self.egress_subproc_cid)

    # def get_ingress_op(self):
    #     return self.meshClient.get(self.ingress_op)

    # def get_integration_op(self):
    #     return self.meshClient.get(self.integration_op)

    # def get_egress_op(self):
    #     return self.meshClient.get(self.egress_op)

    def initBOMcar(self, function_cid, data_cid, init_bom_filename, structure_cid=None, structure_path=None):
        self.init_bom_car_cid, self.init_bom_json_cid = self.meshClient.initBOMcar(
            # structure_path=self.MeshClient.g,
            structure_cid=structure_cid,
            function_cid=function_cid,
            data_cid=data_cid,
            init_bom_filename=init_bom_filename
        )
        self.enhanced_bom, init_bom = self.meshClient.getEnhancedBom(bom_json_cid=self.init_bom_json_cid)
        order = self.enhanced_bom['order']
        # order['ingress_cid'] = 'ipfs://QmVMuxtrhEvzYugy9V3cNmG4Hx38hBXMFVkbB6vyUtZzFc:/inputs/data.tar.gz'
        # order['ingress_cid'] = 'QmVMuxtrhEvzYugy9V3cNmG4Hx38hBXMFVkbB6vyUtZzFc'
        self.enhanced_bom['order'] = order
        self.order_cid = self.enhanced_bom['invoice']['order_cid']
        self.init_bom_json_cid = self.enhanced_bom['bom_json_cid']
        self.bom_json_cid = self.init_bom_json_cid
        return self.init_bom_car_cid, self.init_bom_json_cid
