import json
import pickle
import subprocess
from copy import deepcopy
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
        order = json.loads(self.meshClient.cat(bom["order_cid"]))
        pprint(order)
        ppost = lambda args, endpoint: \
            f'curl -X POST -H "Content-Type: application/json" -d \\\n\'{json.dumps(**args)}\' {endpoint}'
        post = lambda args, endpoint: \
            'curl -X POST -H "Content-Type: application/json" -d \'' + json.dumps(**args) + f'\' {endpoint}'

        post_cmd = post({'obj': bom}, order["endpoint"])
        print(ppost({'obj': bom, 'indent': 4}, order["endpoint"]))
        response_str = subprocess.check_output(post_cmd, shell=True)
        output_bom = json.loads(response_str)
        # pprint(output_bom)
        # exit()

        output_bom['POST'] = post_cmd
        return output_bom

    def flatten_bom(self, bom_response):
        invoice = json.loads(
            self.meshClient.cat(bom_response["bom"]["invoice_cid"])
        )
        invoice['order'] = json.loads(
            self.meshClient.cat(invoice['order_cid']),
        )
        invoice['order']['flat'] = {
            'function': json.loads(self.meshClient.cat(invoice['order']["function_cid"])),
            'invoice': json.loads(self.meshClient.cat(invoice['order']["invoice_cid"]))
        }
        bom_response["flat_bom"] = {
            'invoice': invoice,
            'log': json.loads(
                self.meshClient.cat(bom_response["bom"]["log_cid"])
            )
        }
        return bom_response


    def create_order_request(self,
            process_obj, data_dirpath, structure_filepath,
            endpoint='http://127.0.0.1:5000/cat/node/execute'
    ):
        structure_cid, structure_name = self.meshClient.cidFile(structure_filepath)
        function = {
            'process_cid': self.ipfsClient.add_pyobj(process_obj),
            'infrafunction_cid': None
        }
        invoice = {
            "data_cid": self.meshClient.cidDir(data_dirpath)
        }
        order = {
            "function_cid": self.ipfsClient.add_str(json.dumps(function)),
            "structure_cid": structure_cid,
            "invoice_cid": self.ipfsClient.add_str(json.dumps(invoice)),
            "structure_filepath": structure_name,
            "endpoint": endpoint
        }
        self.order = {
            'order_cid': self.ipfsClient.add_str(json.dumps(order))
        }
        return self.order

    def linkProcess(self, cat_response, process_obj):
        flattened_bom = self.flatten_bom(cat_response)
        flat_bom = deepcopy(flattened_bom['flat_bom'])
        # invoice = deepcopy(flat_bom['invoice'])
        # data_cid = deepcopy(invoice['data_cid'])
        # order = deepcopy(invoice['order'])
        # pprint(invoice)
        # print()
        # pprint(invoice['order'])
        # print()

        function = {
            'process_cid': self.ipfsClient.add_pyobj(process_obj),
            'infrafunction': None
        }

        invoice = flat_bom['invoice']
        input_invoice = {'data_cid': invoice['data_cid']}
        new_function_cid = self.ipfsClient.add_str(json.dumps(function))
        new_invoice_cid = self.ipfsClient.add_str(json.dumps(input_invoice))
        # pprint(new_invoice)
        # print()

        order = invoice['order']
        order['function_cid'] = new_function_cid
        order['invoice_cid'] = new_invoice_cid
        del order['flat']
        order['endpoint'] = 'http://127.0.0.1:5000/cat/node/link'
        # pprint(order)
        # print()

        order_request = {'order_cid': self.ipfsClient.add_str(json.dumps(order))}
        # pprint(order)
        # print()
        return order_request
