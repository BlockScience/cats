import json
from pprint import pprint

from flask import jsonify

from cats.network import ipfsApi
from process import *

ipfsClient = ipfsApi.Client('127.0.0.1', 5001)

structure_json = ipfsClient.add('main.tf')
structure_cid = structure_json['Hash']
structure_filepath = structure_json['Name']
print(structure_cid)
print()

data_0_list = ipfsClient.add('data')
data_0_json = list(filter(lambda x: x['Name'] == 'data', data_0_list))[-1]
data_0_cid = data_0_json['Hash']
print(data_0_cid)
print()

process_0_cid = ipfsClient.add_pyobj(transform_0)
function_0_cid = ipfsClient.add_str(json.dumps({'process_cid': process_0_cid, 'infrafunction_cid': None}))
print(process_0_cid)
print(function_0_cid)
print()

process_1_cid = ipfsClient.add_pyobj(transform_1)
function_1_cid = ipfsClient.add_str(json.dumps({'process_cid': process_1_cid, 'infrafunction_cid': None}))
print(process_1_cid)
print(function_1_cid)
print()



bom0 = {
    "invoice": {
        "data_cid": data_0_cid
    },
    "order": {
        "function_cid": function_0_cid,
        "structure_cid": structure_cid,
        "structure_filepath": structure_filepath
    }
}
pprint(bom0)
print()
print('curl -X POST -H "Content-Type: application/json" -d \\')
print("'", json.dumps(bom0) + "' http://127.0.0.1:5000/cat/node/preproc")
print()

bom1 = {
    "invoice": {
        "data_cid": "QmdqnsWkaP5TWfrnj2qSs4maJTApVkuAbyMcoDnMJdhcgg"
    },
    "order": {
        "function_cid": function_1_cid,
        "structure_cid": structure_cid,
        "structure_filepath": structure_filepath
    }
}
pprint(bom1)
print()
print('curl -X POST -H "Content-Type: application/json" -d \\')
print("'", json.dumps(bom1) + "' http://127.0.0.1:5000/cat/node/postproc")


