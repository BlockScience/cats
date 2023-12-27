import subprocess
from pprint import pprint

import ipfsApi

from cats import CWD
from cats.network import MeshClient
from cats.service import Service
from cats.executor import Executor

subprocess.Popen('terraform destroy --auto-approve', shell=True).wait()
subprocess.call('ipfs daemon', shell=True)

service = Service(
    meshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    )
)
print(f'{CWD}/')
init_bom_car_cid, init_bom_json_cid = service.initBOMcar(
    structure_cid=service.ipfsClient.add(f'main.tf'),
    function_cid='b',
    data_cid='QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp',
    init_bom_filename=f'../old/bom.car'  # include filename in bom
)
catExe = Executor(service=service)
enhanced_bom, bom = catExe.execute(init_bom_json_cid)

print(service.order_cid)
print()
pprint(bom)
print()
pprint(enhanced_bom)
print()
prev_enhanced_bom = {
    'bom_json_cid': 'QmXX9wEoRzSeJixp2isrRuLb9KJpprVw1DcJ2eVePzukMW',
    'invoice': {
        'data_cid': 'QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp',
        'order_cid': 'QmangQmYjjrLGEfVZ7yBe2u1eqrnzqSsxVuYSzsyuPCYZv',
        'seed_cid': None
    },
    'invoice_cid': 'QmNRHK4P5kWpsKda8NzpV7c7Qj9L4ppQZbYJc2iFvn7rLf',
    'log_cid': None,
    'order': {
        'function_cid': 'b',
        'invoice_cid': 'QmbUD6XRVS8UbEc9LyBsj7d5M5sQ9WxnquguFEF8AM6wWZ',
        'structure_cid': {
            'Hash': 'QmcrLhZMZMYAhLMz8mWzDriPoB5axwxXeE5JJmPBjAtDFa',
            'Name': 'main.tf',
            'Size': '1886'
        }
    }
}
print(enhanced_bom == prev_enhanced_bom)
