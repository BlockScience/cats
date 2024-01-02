import json
import pickle
from copy import deepcopy
from pprint import pprint

from flask import Flask, request, jsonify
cat = Flask(__name__)

from cats.network import ipfsApi, MeshClient
from cats.service import Service
from cats.factory import Factory

service = Service(
    meshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    )
)

def initFactory(order_request, ipfs_uri):
    # if cod_out is False:
    #     ipfs_uri = f'ipfs://{order_request["invoice"]["data_cid"]}/*csv'
    # elif cod_out is True:
    #     ipfs_uri = f'ipfs://{order_request["invoice"]["data_cid"]}/output/*csv'
    service.initBOMcar(
        structure_cid=order_request['order']['structure_cid'],
        structure_filepath=order_request['order']['structure_filepath'],
        function_cid=order_request['order']['function_cid'],
        init_data_cid=ipfs_uri
    )
    catFactory = Factory(service)
    return catFactory, order_request

def execute(catFactory, order_request):
    enhanced_bom = catFactory.execute()

    invoice = {}
    enhanced_bom['invoice']['order_cid'] = service.ipfsClient.add_str(
        json.dumps(order_request['order'])
    )
    invoice['invoice_cid'] = service.ipfsClient.add_str(
        json.dumps(enhanced_bom['invoice'])
    )
    invoice['invoice'] = enhanced_bom['invoice']

    bom = {
        'log_cid': enhanced_bom['log_cid'],
        'invoice_cid': invoice['invoice_cid']
    }
    bom_response = {
        'bom': bom,
        'bom_cid': service.ipfsClient.add_str(json.dumps(bom))
    }
    return bom_response


@cat.route('/cat/node/init', methods=['POST'])
def execute_init_cat():
    try:
        # Get JSON data from the request
        order_request = request.get_json()
        order_request["order"] = json.loads(service.meshClient.cat(order_request["order_cid"]))
        order_request['invoice'] = json.loads(service.meshClient.cat(order_request['order']['invoice_cid']))
        pprint(order_request["order"])
        pprint(order_request['invoice']['data_cid'])



        # bom['invoice']['data_cid'] = service.meshClient.linkData(bom['invoice']['data_cid'])

        # IPFS checks
        # if 'bom_cid' not in bom:
        #     return jsonify({'error': 'CID not provided'}), 400


        ipfs_uri = f'ipfs://{order_request["invoice"]["data_cid"]}/*csv'
        catFactory, updated_order_request = initFactory(order_request, ipfs_uri)
        bom_response = execute(catFactory, updated_order_request)

        # Return BOM
        return jsonify(bom_response)

    except Exception as e:
        return jsonify({'error': str(e)})

@cat.route('/cat/node/link', methods=['POST'])
def execute_link_cat():
    try:
        # Get JSON data from the request
        order_request = request.get_json()
        order_request["order"] = json.loads(service.meshClient.cat(order_request["order_cid"]))
        order_request['invoice'] = json.loads(service.meshClient.cat(order_request['order']['invoice_cid']))
        pprint(order_request["order"])
        pprint(order_request['invoice']['data_cid'])

        prev_data_cid = order_request['invoice']['data_cid']
        data_cid = service.meshClient.linkData(prev_data_cid)
        ipfs_uri = f'ipfs://{data_cid}/*csv'
        catFactory, updated_order_request = initFactory(order_request, ipfs_uri)
        bom_response = execute(catFactory, updated_order_request)

        # Return BOM
        return jsonify(bom_response)

        # Return BOM
        return jsonify(bom_response)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Run the Flask application on http://127.0.0.1:5000/
    cat.run(debug=True)