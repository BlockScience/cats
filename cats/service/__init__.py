import json
import pickle
from copy import copy, deepcopy
from pprint import pprint

from cats.service.utils import executeCMD
from cats.network import ipfsApi
from cats.network import MeshClient


class Service:
    def __init__(self,
        meshClient: MeshClient
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
        self.process = None
        self.dataCID = None

    # # ToDo: EP: (Init) CAT
    # def serve(self, response):
    #     self.executor: Executor = Factory(response.json)
    #     self.executor.execute()

    def initBOMcar(self, function_cid, init_data_cid, init_bom_filename='bom.car', structure_cid=None, structure_filepath=None):
        self.init_bom_car_cid, self.init_bom_json_cid = self.meshClient.initBOMcar(
            # structure_path=self.MeshClient.g,
            structure_cid=structure_cid,
            structure_filepath=structure_filepath,
            function_cid=function_cid,
            init_data_cid=init_data_cid,
            init_bom_filename=init_bom_filename
        )
        self.enhanced_bom, init_bom = self.meshClient.getEnhancedBom(bom_json_cid=self.init_bom_json_cid)
        # self.processCID = deepcopy(self.enhanced_bom['order']['function_cid'])
        # pprint(self.enhanced_bom)
        # exit()

        self.functionCID = self.enhanced_bom['order']['function_cid']
        function_dict = json.loads(self.meshClient.cat(self.functionCID))
        self.processCID = function_dict['process_cid']
        self.process = pickle.loads(self.meshClient.catObj(self.processCID))
        # self.enhanced_bom['order']['function_cid'] = self.functionCID
        # self.process = self.ipfsClient.get_pyobj(self.processCID)
        # order = self.enhanced_bom['order']
        # order['ingress_cid'] = 'ipfs://QmVMuxtrhEvzYugy9V3cNmG4Hx38hBXMFVkbB6vyUtZzFc:/inputs/data.tar.gz'
        # order['ingress_cid'] = 'QmVMuxtrhEvzYugy9V3cNmG4Hx38hBXMFVkbB6vyUtZzFc'
        # self.enhanced_bom['order'] = order

        self.order_cid = self.enhanced_bom['invoice']['order_cid']
        self.init_bom_json_cid = self.enhanced_bom['bom_json_cid']
        self.bom_json_cid = self.init_bom_json_cid
        return self.init_bom_car_cid, self.init_bom_json_cid
