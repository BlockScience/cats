import json
import pickle
import subprocess
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
        self.bom_json_cid = None
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

    def catSubmit(self, bom):
        ppost = lambda args, endpoint: \
            f'curl -X POST -H "Content-Type: application/json" -d \\\n\'{json.dumps(**args)}\' {endpoint}'
        post = lambda args, endpoint: \
            'curl -X POST -H "Content-Type: application/json" -d \'' + json.dumps(**args) + f'\' {endpoint}'
        post_cmd = post({'obj': bom}, bom["order"]["endpoint"])
        print(ppost({'obj': bom, 'indent': 4}, bom["order"]["endpoint"]))
        response_str = subprocess.check_output(post_cmd, shell=True)
        output_bom = json.loads(response_str)
        # pprint(output_bom)
        # exit()

        output_bom['POST'] = post_cmd
        return output_bom

    def resubmit_bom(self,
        bom, endpoint='http://127.0.0.1:5000/cat/node/postproc'
    ):
        def f(
                process_obj, invoice_bom=bom,
                endpoint=endpoint
        ):
            order_bom = deepcopy(invoice_bom)
            del order_bom["order"]["invoice_cid"]
            order_bom["function"]['process_cid'] = self.ipfsClient.add_pyobj(process_obj)
            order_bom["order"]["function_cid"] = self.ipfsClient.add_str(json.dumps(order_bom["function"]))
            order_bom["order"]["endpoint"] = endpoint
            return order_bom

        return f

    def create_order(self,
            process_obj, data_dirpath, structure_filepath,
            endpoint='http://127.0.0.1:5000/cat/node/preproc'
    ):
        structure_cid, structure_name = self.meshClient.cidFile(structure_filepath)
        function = {
            'process_cid': self.ipfsClient.add_pyobj(process_obj),
            'infrafunction_cid': None
        }
        order_bom = {
            "invoice": {
                "data_cid": self.meshClient.cidDir(data_dirpath)
            },
            "order": {
                "function_cid": self.ipfsClient.add_str(json.dumps(function)),
                "structure_cid": structure_cid,
                "structure_filepath": structure_name,
                "endpoint": endpoint
            },
            "function": function
        }
        self.order = order_bom
        return self.order

    def catJob_repl(self,
            previous_invoice_bom, modify_bom,
            endpoint='http://127.0.0.1:5000/cat/node/postproc'
    ):
        def resubmit_catJob(
                process_obj
        ):
            def resubmit_order(process_obj=process_obj):
                order_bom = modify_bom(process_obj, previous_invoice_bom, endpoint)
                return order_bom, self.catSubmit(order_bom)

            order_bom, invoice_bom = resubmit_order(process_obj)
            return order_bom, invoice_bom, resubmit_order

        return resubmit_catJob

    def cat_repl(self,
            order_bom, bom_function,
            endpoint='http://127.0.0.1:5000/cat/node'
    ):
        preproc_endpoint = f'{endpoint}/preproc'
        # order_bom["order"]['endpoint'] = preproc_endpoint
        pprint(order_bom)
        invoice_bom = self.catSubmit(order_bom)

        postproc_endpoint = f'{endpoint}/postproc'
        catJobRepl = self.catJob_repl(invoice_bom, bom_function, postproc_endpoint)
        return order_bom, invoice_bom, catJobRepl

