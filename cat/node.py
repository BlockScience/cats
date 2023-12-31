from flask import Flask, request, jsonify
cat = Flask(__name__)

from cats.network import ipfsApi, MeshClient
from cats.service import Service
from cats.executor import Executor
from cats.factory import Factory

service = Service(
    meshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    )
)


@cat.route('/cat/node/preproc', methods=['POST'])
def initExecute():
    try:
        # Get JSON data from the request
        bom = request.get_json()

        # IPFS checks
        # if 'init_data_cid' not in bom:
        #     return jsonify({'error': 'CID not provided'}), 400

        data_cid = bom['invoice']['data_cid']
        ipfs_uri = f'ipfs://{data_cid}/*csv'
        service.initBOMcar(
            structure_cid=bom['order']['structure_cid'],
            structure_filepath=bom['order']['structure_filepath'],
            function_cid=bom['order']['function_cid'],
            init_data_cid=ipfs_uri
        )
        catFactory = Factory(service)
        enhanced_bom = catFactory.execute()

        # Return BOM
        return jsonify(enhanced_bom)

    except Exception as e:
        return jsonify({'error': str(e)})

@cat.route('/cat/node/postproc', methods=['POST'])
def execute():
    try:
        # Get JSON data from the request
        bom = request.get_json()


        # IPFS checks
        # if 'bom_json_cid' not in bom:
        #     return jsonify({'error': 'CID not provided'}), 400

        data_cid = service.meshClient.linkData(bom['invoice']['data_cid'])
        ipfs_uri = f'ipfs://{data_cid}/*csv'
        service.initBOMcar(
            structure_cid=bom['order']['structure_cid'],
            structure_filepath=bom['order']['structure_filepath'],
            function_cid=bom['order']['function_cid'],
            init_data_cid=ipfs_uri
        )
        catFactory = Factory(service)
        enhanced_bom = catFactory.execute()

        # Return BOM
        return jsonify(enhanced_bom)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Run the Flask application on http://127.0.0.1:5000/
    cat.run(debug=True)