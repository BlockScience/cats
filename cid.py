import json
from pprint import pprint

from cats.network import ipfsApi, MeshClient
from cats.service import Service
from process import *

service = Service(
    meshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    )
)

order_bom_0 = service.create_order(
    process_obj=process_0,
    data_dirpath='data',
    structure_filepath='main.tf',
    endpoint='http://127.0.0.1:5000/cat/node/preproc'
)


def modify_bom(
        process_obj, invoice_bom,
        endpoint='http://127.0.0.1:5000/cat/node/postproc'
):
    order_bom = {}
    order_bom["order"] = invoice_bom["order"]
    del order_bom["order"]["invoice_cid"]
    order_bom["invoice"] = {'data_cid': invoice_bom["invoice"]["data_cid"]}
    order_bom["function"] = invoice_bom["function"]
    order_bom["function"]['process_cid'] = service.ipfsClient.add_pyobj(process_obj)
    order_bom["order"]["function_cid"] = service.ipfsClient.add_str(json.dumps(order_bom["function"]))
    order_bom["order"]["endpoint"] = endpoint
    return order_bom


cat_0 = order_bom_0, invoice_bom_0, modified_catJob_0 = service.cat_repl(
    order_bom=order_bom_0,
    bom_function=modify_bom
)
pprint(order_bom_0)
print()
pprint(invoice_bom_0)
print()
print()

cat_1 = order_bom_1, invoice_bom_1, modified_catJob_1 = modified_catJob_0(
    process_obj=process_1
)
pprint(order_bom_1)
print()
pprint(invoice_bom_1)
print()
print()
print(invoice_bom_0['POST'])
#

