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

# ipfsClient = ipfsApi.Client('127.0.0.1', 5001)


# def cidFile(filepath):
#     file_json = ipfsClient.add(filepath)
#     file_cid = file_json['Hash']
#     file_name = file_json['Name']
#     return file_cid, file_name
#
#
# def cidDir(filepath):
#     data = ipfsClient.add(filepath)
#     if type(data) is list:
#         data_json = list(filter(lambda x: x['Name'] == filepath, data))[-1]
#         data_cid = data_json['Hash']
#         return data_cid
#     else:
#         data_json = data
#         data_cid = data_json['Hash']
#         return data_cid
#
#
# def catSubmit(bom):
#     ppost = lambda args, endpoint: \
#         f'curl -X POST -H "Content-Type: application/json" -d \\\n\'{json.dumps(**args)}\' {endpoint}'
#     post = lambda args, endpoint: \
#         'curl -X POST -H "Content-Type: application/json" -d \''+json.dumps(**args)+f'\' {endpoint}'
#     post_cmd = post({'obj': bom}, bom["order"]["endpoint"])
#     print(ppost({'obj': bom, 'indent': 4}, bom["order"]["endpoint"]))
#     response_str = subprocess.check_output(post_cmd, shell=True)
#     output_bom = json.loads(response_str)
#     output_bom['POST'] = post_cmd
#     return output_bom
#
#
# def create_order(
#         process_obj, data_dirpath, structure_filepath,
#         endpoint='http://127.0.0.1:5000/cat/node/preproc'
# ):
#     structure_cid, structure_name = cidFile(structure_filepath)
#     function = {
#         'process_cid': ipfsClient.add_pyobj(process_obj),
#         'infrafunction_cid': None
#     }
#     order_bom = {
#         "invoice": {
#             "data_cid": cidDir(data_dirpath)
#         },
#         "order": {
#             "function_cid": ipfsClient.add_str(json.dumps(function)),
#             "structure_cid": structure_cid,
#             "structure_filepath": structure_name,
#             "endpoint": endpoint
#         },
#         "function": function
#     }
#     return order_bom
#
#
# def catJob_repl(
#         previous_bom, modify_bom,
#         endpoint='http://127.0.0.1:5000/cat/node/postproc'
# ):
#     def resubmit_catJob(
#             process_obj
#     ):
#         def resubmit_order(process_obj=process_obj):
#             order_bom = modify_bom(process_obj, previous_bom, endpoint)
#             return order_bom, catSubmit(order_bom)
#         order_bom, invoice_bom = resubmit_order(process_obj)
#         return order_bom, invoice_bom, resubmit_order
#     return resubmit_catJob
#
#
#
# def cat_repl(
#     order_bom, bom_function,
#     endpoint='http://127.0.0.1:5000/cat/node'
# ):
#     preproc_endpoint = f'{endpoint}/preproc'
#     order_bom["order"]['endpoint'] = preproc_endpoint
#     invoice_bom = catSubmit(order_bom)
#
#     postproc_endpoint = f'{endpoint}/postproc'
#     catJobRepl = catJob_repl(invoice_bom, bom_function, postproc_endpoint)
#     return order_bom, invoice_bom, catJobRepl


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

# def resubmit_bom(
#         bom,
#         endpoint='http://127.0.0.1:5000/cat/node/postproc'
# ):
#     def f(
#             process_obj, invoice_bom=bom,
#             endpoint=endpoint
#     ):
#         order_bom = deepcopy(invoice_bom)
#         del order_bom["order"]["invoice_cid"]
#         order_bom["function"]['process_cid'] = ipfsClient.add_pyobj(process_obj)
#         order_bom["order"]["function_cid"] = ipfsClient.add_str(json.dumps(order_bom["function"]))
#         order_bom["order"]["endpoint"] = endpoint
#         return order_bom
#     return f
# resubmitBom = resubmit_bom(order_bom_0)
# cat_a = order_bom_a, invoice_bom_a, process_loader_catJob = cat_repl(
#     order_bom=order_bom_0,
#     bom_function=resubmitBom
# )
# cat_b = order_bom_b, invoice_bom_b, _ = process_loader_catJob(
#     process_obj=process_1
# )
# cat_c = order_bom_c, invoice_bom_c, _ = process_loader_catJob(
#     process_obj=process_1
# )



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

