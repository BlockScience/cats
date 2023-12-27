from flask import Flask, request, jsonify
cat = Flask(__name__)
cat.debug = True

from cats.network import ipfsApi, MeshClient
from cats.service import Service
from cats.executor import Executor

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
        structure_cid = bom['order']['structure_cid']
        structure_filepath = bom['order']['structure_filepath']
        function_cid = bom['order']['function_cid']

        service.initBOMcar(
            structure_cid=structure_cid,
            structure_filepath=structure_filepath,
            function_cid=function_cid,
            init_data_cid=ipfs_uri
        )

        catExe = Executor(service=service)
        enhanced_bom, _ = catExe.execute()

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

        prev_data_cid = bom['invoice']['data_cid']
        data_cid = service.meshClient.linkData(prev_data_cid)
        ipfs_uri = f'ipfs://{data_cid}/*csv'
        structure_json = service.ipfsClient.add(bom['order']['structure_filepath'])
        function_cid = bom['order']['function_cid']
        service.initBOMcar(
            structure_cid=structure_json['Hash'],
            structure_filepath=structure_json['Name'],
            # function_cid=service.ipfsClient.add_str(function_json),
            function_cid=function_cid,
            init_data_cid=ipfs_uri
        )
        catExe = Executor(service=service)
        enhanced_bom, _ = catExe.execute()


        # Return BOM
        return jsonify(enhanced_bom)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # Run the Flask application on http://127.0.0.1:5000/
    cat.run(debug=True)