import json
import os
import subprocess
from copy import copy, deepcopy
from pprint import pprint

import w3storage
from dag_json import decode, encode
from multiformats import CID
import ipfsApi
api = ipfsApi.Client('127.0.0.1', 5001)
# w3_api_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDE4OTMzQzE5MjAwNGExNWNkN2ZjZjc5MTJENjZlZDc5MzU2Mzk5MjAiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2ODk1NDg3MTE3ODEsIm5hbWUiOiJjYXRzIn0.2nEPdntKra6K6QSI0nLGQbf9olOQH-zt8ypfKYg_WWw'
# w3 = w3storage.API(token=w3_api_token)
# pprint(api.id())
# api.cat('QmevA4DgJqSvNn1EEFo45kLAbwxnutRxRTDuguKShxXwTJ')

def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

def init_bom_json(structure_cid: str, function_cid: str, data_cid: str, seed_cid = None):
    init_invoice = {
        'order_cid': None,
        'data_cid': data_cid,
        'seed_cid': seed_cid,
    }
    init_order = {
        'invoice_cid': None,
        'function_cid': function_cid,
        'structure_cid': structure_cid
    }

    init_invoice_cid = api.add_json(init_invoice)
    init_order['invoice_cid'] = init_invoice_cid
    init_order_cid = api.add_json(init_order)

    invoice = copy(init_invoice)
    invoice['order_cid'] = init_order_cid
    invoice_cid = api.add_json(invoice)

    init_bom = {
        'invoice_cid': invoice_cid,
        'log_cid': None,
    }
    init_bom_cid = api.add_json(init_bom)
    return init_bom_cid

def get_bom_file(bom_cid: str, filepath: str):
    subprocess.check_output(
        f"ipfs get {bom_cid}",
        stderr=subprocess.STDOUT,
        shell=True
    )
    os.rename(bom_cid, filepath)

def get_bom_car(bom_cid: str, filepath: str):
    subprocess.check_output(
        f"ipfs dag export {bom_cid} > {filepath}",
        stderr=subprocess.STDOUT,
        shell=True
    )

def get_bom(bom_cid: str, filepath: str):
    get_bom_file(bom_cid, filepath)
    bom = dict(json.loads(filepath))
    subprocess.check_output(
        f"rm {filepath}",
        stderr=subprocess.STDOUT,
        shell=True
    )
    return bom

w3_api_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweDE4OTMzQzE5MjAwNGExNWNkN2ZjZjc5MTJENjZlZDc5MzU2Mzk5MjAiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2ODk1NDg3MTE3ODEsIm5hbWUiOiJjYXRzIn0.2nEPdntKra6K6QSI0nLGQbf9olOQH-zt8ypfKYg_WWw'
w3 = w3storage.API(token=w3_api_token)
def transfer_bom_to_w3(bom_cid: str, filepath: str, w3_api_token: str):
    get_bom_car(bom_cid, filepath)
    w3 = w3storage.API(token=w3_api_token)
    w3_bom_cid = w3.post_upload(filepath)
    return w3_bom_cid, bom_cid

def convert_bom(bom_cid: str, filepath: str):
    # get_bom(bom_cid, filepath)
    get_bom_car(bom_cid, filepath)
    car_bom_cid = api.add(filepath)['Hash']
    return car_bom_cid, bom_cid

def init_bom_car(structure_cid: str, function_cid: str, data_cid: str, init_bom_filename: str, seed_cid = None):
    init_bom_json_cid = init_bom_json(structure_cid, function_cid, data_cid)
    car_bom_cid, init_bom_json_cid = convert_bom(init_bom_json_cid, init_bom_filename)
    return car_bom_cid, init_bom_json_cid


def get_enhanced_bom(bom_json_cid: str):
    get_bom_file(bom_json_cid, 'bom.json')
    bom = json.loads(open('bom.json', 'r').read())
    enhanced_bom = deepcopy(bom)
    enhanced_bom['bom_json_cid'] = bom_json_cid

    get_bom_file(bom['invoice_cid'], '../invoice.json')
    enhanced_bom['invoice'] = json.loads(open('../invoice.json', 'r').read())

    get_bom_file(enhanced_bom['invoice']['order_cid'], '../order.json')
    enhanced_bom['order'] = json.loads(open('../order.json', 'r').read())

    get_bom_file(enhanced_bom['order']['structure_cid']['Hash'], enhanced_bom['order']['structure_cid']['Name'])
    return enhanced_bom, bom


def executeStructure(bom_json_cid: str):
    enhanced_bom, bom = get_enhanced_bom(bom_json_cid)

    for path in execute(['terraform', 'destroy', '--auto-approve']):
        print(path, end="")
    for path in execute(['terraform', 'init', '--upgrade']):
        print(path, end="")
    for path in execute(['terraform', 'apply', '--auto-approve']):
        print(path, end="")
    for path in execute(['terraform', 'destroy', '--auto-approve']):
        print(path, end="")

    return enhanced_bom, bom


structure_cid = api.add('main.tf')
data_cid = 'QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'
init_bom_filename = 'bom.car'
# include filename in bom
car_bom_cid, init_bom_json_cid = init_bom_car(structure_cid, 'b', data_cid, init_bom_filename)


enhanced_bom, bom = executeStructure(init_bom_json_cid)

# print(init_bom_json_cid)
# print(car_bom_cid)
pprint(bom)
pprint(enhanced_bom)



# car_bom_cid, init_bom_json_cid = init_bom_car(structure_cid, 'b', data_cid, init_bom_filename)
# print(init_bom_json_cid)
# print(car_bom_cid)
#
# bom_filename = 'bom.json'
# get_bom_file(init_bom_json_cid, bom_filename)
# j = json.loads(open(bom_filename, 'r').read())
# pprint(j)
# def init_bom_car_to_w3(structure_cid: str, function_cid: str, data_cid: str, init_bom_filename: str, seed_cid = None):
#     init_bom_car_cid, init_bom_json_cid = init_bom_car(function_cid, structure_cid, data_cid, init_bom_filename)
#     w3_bom_cid, init_bom_json_cid = transfer_bom_to_w3(init_bom_car_cid, init_bom_filename)
#     return car_bom_cid, init_bom_json_cid


# help(json.dumps)

# pprint(())
#
# def get_dict(cid):
#     print(cid)
#     # help(api)
#     return api.cat(cid)
#
# get_dict(cid)

# encoded_order = encode({
#     'order_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
#     'invoice_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
#     'function_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
#     'structure_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp')
# })
#
# order = {
#     'order_cid': 'QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp',
#     'invoice_cid': 'QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp',
#     'function_cid': 'QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp',
#     'structure_cid': 'QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'
# }

    # encoded_init_invoice = encode(
    #     {
    #         'order_cid': None,
    #         'data_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
    #         'seed_cid': None,
    #     }
    # )
    # decoded_init_invoice = decode(encoded_init_invoice)
    # ipld_init_invoice_cid = api.add_pyobj(decoded_init_invoice)
    # return ipld_init_invoice_cid
    # return ipld_init_invoice_cid
    # return json.loads(decoded_init_invoice)
    # return str(decoded_init_invoice['data_cid'])
    # init_invoice_cid = api.add_json(
    #     {
    #         'order_cid': None,
    #         'data_cid': data_cid,
    #         'seed_cid': None,
    #     }
    # )
    # return init_invoice_cid
    # init_invoice_cid = encoded_cid(encoded_init_invoice)
    # encoded_init_invoice = repr(decode(encoded_init_invoice))
    # encoded_init_invoice['invoice_cid']

# cid_init_invoice('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp')

# encoded_init_invoice =  enco
# de_init_invoice('')
#
# encoded_invoice = encode({
#     'invoice_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
#     'order_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
#     'data_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
#     'seed_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp')
# })
#
# encoded_bom = encode({
#     'bom_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
#     'invoice_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
#     'log_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp')
# })