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

    def resubmit_bom(self,
        bom, endpoint='http://127.0.0.1:5000/cat/node/process'
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

    def process_loader(self, process_obj, invoice_bom, endpoint):
        new_order_bom = {}
        new_order_bom["order"] = json.loads(self.meshClient.cat(invoice_bom["order_cid"]))
        new_order_bom["order"]["endpoint"] = endpoint
        new_order_bom["function"] = json.loads(self.meshClient.cat(new_order_bom["order"]["function_cid"]))
        new_order_bom["function"]['process_cid'] = self.ipfsClient.add_pyobj(process_obj)
        new_order_bom["order"]["function_cid"] = self.ipfsClient.add_str(json.dumps(new_order_bom["function"]))
        new_order_bom["order_cid"] = self.ipfsClient.add_str(json.dumps(new_order_bom["order"]))
        # new_order_bom["order"] = json.loads(self.meshClient.cat(new_order_bom["order_cid"]))
        del new_order_bom["function"]
        # next_invoice = {
        #     'data_cid': invoice_bom['data_cid']
        # }
        #
        # new_order_bom["order"]['invoice'] = next_invoice
        # new_order_bom["order"]['invoice']['invoice_cid'] = self.ipfsClient.add_str(json.dumps(next_invoice))
        new_order_bom["invoice"] = invoice_bom
        del new_order_bom['invoice']['order_cid']
        del new_order_bom['invoice']['seed_cid']
        new_order_bom['order']['invoice_cid'] = self.ipfsClient.add_str(json.dumps(new_order_bom['invoice']))
        new_order_bom['invoice'] = new_order_bom['invoice']
        return new_order_bom

    def catJob_repl(self,
                    previous_invoice, structured_function,
                    endpoint='http://127.0.0.1:5000/cat/node/process'
                    ):
        def resubmit_order(
                process_obj
        ):
            def f(process_obj=process_obj):
                order_request = structured_function(
                    service=self,
                    process_obj=process_obj,
                    invoice=previous_invoice,
                    endpoint=endpoint
                )
                # del order_request['order']
                # del order_request['invoice']
                pprint(order_request)
                print()
                cat_response = self.catSubmit(order_request)
                pprint(cat_response)
                # exit()
                return self.flatten_bom(cat_response)
            flat_cat_response = f(process_obj)
            flat_cat_response['cat_processor'] = f
            return flat_cat_response

        return resubmit_order

    def cat_repl(self,
            order_bom, structured_function,
            endpoint='http://127.0.0.1:5000/cat/node'
    ):
        # preproc_endpoint = f'{endpoint}/execute'
        # order_bom["order"]['endpoint'] = preproc_endpoint
        cat_response = self.catSubmit(order_bom)
        flat_cat_response = self.flatten_bom(cat_response)

        postproc_endpoint = f'{endpoint}/process'
        # invoice = flat_cat_response['flat_bom']['invoice']
        invoice = json.loads(self.meshClient.cat(flat_cat_response['bom']["invoice_cid"]))
        # pprint(invoice)
        # print()
        # exit()
        catJobRepl = self.catJob_repl(invoice, structured_function, postproc_endpoint)
        flat_cat_response['cat_processor'] = catJobRepl
        return flat_cat_response

