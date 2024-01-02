```python
import json
from pprint import pprint
from copy import deepcopy
from cats.network import ipfsApi, MeshClient
from cats.service import Service
from process import *
```

    /home/jjodesty/Projects/Research/cats-research/cats/network/__init__.py:6: FutureWarning: The `ipfsapi` library is deprecated and will stop receiving updates on the 31.12.2019! If you are on Python 3.5+ please enable and fix all Python deprecation warnings (CPython flag `-Wd`) and switch to the new `ipfshttpclient` library name. Python 2.7 and 3.4 will not be supported by the new library, so please upgrade.
      import ipfsapi as ipfsApi
    /home/jjodesty/Projects/Research/cats-research/venv/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
      from .autonotebook import tqdm as notebook_tqdm
    2024-01-01 20:28:00,299	INFO util.py:159 -- Missing packages: ['ipywidgets']. Run `pip install -U ipywidgets`, then restart the notebook server for rich notebook output.



```python
service = Service(
    meshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    )
)
```


```python
cat_order_request_0 = service.create_order_request(
    process_obj=process_0,
    data_dirpath='data',
    structure_filepath='main.tf',
    endpoint='http://127.0.0.1:5000/cat/node/init'
)
pprint(cat_order_request_0)
```

    {'order_cid': 'QmSmGTZTUaFyhxdfp8uLrAWPvkREmRq1vxbnPYEVTvw2Xu'}



```python
cat_invoiced_response_0 = service.catSubmit(cat_order_request_0)
# pprint(cat_invoiced_response_0)
flat_cat_invoiced_response_0 = service.flatten_bom(cat_invoiced_response_0)
pprint(flat_cat_invoiced_response_0)
```

    {'endpoint': 'http://127.0.0.1:5000/cat/node/init',
     'function_cid': 'QmPMniqGmZ28QnDwa2UJqkcWjkkaehkEKcXD47kLUVWaEd',
     'invoice_cid': 'QmQnZ1DR9CMjcyzH5RpD9mMcg39AMyjf2mRNEwj8tPHBMJ',
     'structure_cid': 'QmYyFroE2Nw1BVg3D1MQdeZFrMAn9XWYHgWueMUKaRGops',
     'structure_filepath': 'main.tf'}
    curl -X POST -H "Content-Type: application/json" -d \
    '{
        "order_cid": "QmSmGTZTUaFyhxdfp8uLrAWPvkREmRq1vxbnPYEVTvw2Xu"
    }' http://127.0.0.1:5000/cat/node/init


      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100   278  100   215    0    63      2      0  0:01:47  0:01:33  0:00:14    52


    {'POST': 'curl -X POST -H "Content-Type: application/json" -d \'{"order_cid": '
             '"QmSmGTZTUaFyhxdfp8uLrAWPvkREmRq1vxbnPYEVTvw2Xu"}\' '
             'http://127.0.0.1:5000/cat/node/init',
     'bom': {'invoice_cid': 'QmaSukf5bKcy7csEokXp4WQAWSR1MC2C53hppcE5tuvj6u',
             'log_cid': 'QmckWJ5jxjTeE811xLsAzz4NYPyxdWvG5GF3pc1rBitJuT'},
     'bom_cid': 'QmeeLJJXG8N41q7caqvTQAznNGEhxa6CMH45QZFWjg84pF',
     'flat_bom': {'invoice': {'data_cid': 'QmSCDXRUhPjkUShYJotqtqaMNRCs4QDSKG4hhh8qqiYfXh',
                              'order': {'endpoint': 'http://127.0.0.1:5000/cat/node/init',
                                        'flat': {'function': {'infrafunction_cid': None,
                                                              'process_cid': 'QmXqKpSVBuoZD2QG8hT3tTF8ai6cHV8iTHt2tF5sM3scmc'},
                                                 'invoice': {'data_cid': 'QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN'}},
                                        'function_cid': 'QmPMniqGmZ28QnDwa2UJqkcWjkkaehkEKcXD47kLUVWaEd',
                                        'invoice_cid': 'QmQnZ1DR9CMjcyzH5RpD9mMcg39AMyjf2mRNEwj8tPHBMJ',
                                        'structure_cid': 'QmYyFroE2Nw1BVg3D1MQdeZFrMAn9XWYHgWueMUKaRGops',
                                        'structure_filepath': 'main.tf'},
                              'order_cid': 'QmSmGTZTUaFyhxdfp8uLrAWPvkREmRq1vxbnPYEVTvw2Xu',
                              'seed_cid': None},
                  'log': {'egress_job_id': 'f5cba3f5-66dd-4538-b8ca-00a3d3199c77',
                          'ingress_job_id': '8c936749-4c5c-41cd-ad60-c07d9c3a2d05',
                          'integration_output': 's3://catstore3/boms/result-20240102-8c936749-4c5c-41cd-ad60-c07d9c3a2d05-integrated'}}}



```python
cat_order_request_1 = service.linkProcess(cat_invoiced_response_0, process_1)
pprint(cat_order_request_1)
```

    {'order_cid': 'QmZkSSpiDjmZtuD3x8qYwLD1YRXEayAau4JAktXX9JotZS'}



```python
cat_invoiced_response_1 = service.catSubmit(cat_order_request_1)
# pprint(cat_invoiced_response_1)
flat_cat_invoiced_response_1 = service.flatten_bom(cat_invoiced_response_1)
pprint(flat_cat_invoiced_response_1)
```

    {'endpoint': 'http://127.0.0.1:5000/cat/node/link',
     'function_cid': 'QmXoU3V8JWvHm12rbsm4czhQAS1k47ESY5Uto1Pqekb87q',
     'invoice_cid': 'QmYofDJeNA8uS5RthFVQKbDDuUJ2XhrsCQ92vKwfX6EpRg',
     'structure_cid': 'QmYyFroE2Nw1BVg3D1MQdeZFrMAn9XWYHgWueMUKaRGops',
     'structure_filepath': 'main.tf'}
    curl -X POST -H "Content-Type: application/json" -d \
    '{
        "order_cid": "QmZkSSpiDjmZtuD3x8qYwLD1YRXEayAau4JAktXX9JotZS"
    }' http://127.0.0.1:5000/cat/node/link


      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100    63    0     0    0    63      0      0 --:--:--  0:02:34 --:--:--     0

    {'POST': 'curl -X POST -H "Content-Type: application/json" -d \'{"order_cid": '
             '"QmZkSSpiDjmZtuD3x8qYwLD1YRXEayAau4JAktXX9JotZS"}\' '
             'http://127.0.0.1:5000/cat/node/link',
     'bom': {'invoice_cid': 'Qmcn8azUCX72ZCsXQWhP93UmZ3wA6CMfen7ZqyHRegpYeD',
             'log_cid': 'QmVsHydhKqgo2eMH4nT6uRfLpgRTxyejKvqys6rb35RPWc'},
     'bom_cid': 'QmXgvwgpKoY7PSfsGgQwx8FsMfFoxTzucyM9kF9tnrYyio',
     'flat_bom': {'invoice': {'data_cid': 'QmYH6ayMBMgi9rvQ2CihgzNkgua2aSo7B7aaBuEHbMZCL2',
                              'order': {'endpoint': 'http://127.0.0.1:5000/cat/node/link',
                                        'flat': {'function': {'infrafunction': None,
                                                              'process_cid': 'QmXC2XLDePUxCoPtETPejd5uwF3BcaoQNAn2vRU4a4BK7z'},
                                                 'invoice': {'data_cid': 'QmSCDXRUhPjkUShYJotqtqaMNRCs4QDSKG4hhh8qqiYfXh'}},
                                        'function_cid': 'QmXoU3V8JWvHm12rbsm4czhQAS1k47ESY5Uto1Pqekb87q',
                                        'invoice_cid': 'QmYofDJeNA8uS5RthFVQKbDDuUJ2XhrsCQ92vKwfX6EpRg',
                                        'structure_cid': 'QmYyFroE2Nw1BVg3D1MQdeZFrMAn9XWYHgWueMUKaRGops',
                                        'structure_filepath': 'main.tf'},
                              'order_cid': 'QmZkSSpiDjmZtuD3x8qYwLD1YRXEayAau4JAktXX9JotZS',
                              'seed_cid': None},
                  'log': {'egress_job_id': 'e5e8ca76-5a6c-4097-a483-c97b8f1f6570',
                          'ingress_job_id': '9a1f5b6c-e3d4-4bed-9368-56d511882835',
                          'integration_output': 's3://catstore3/boms/result-20240102-9a1f5b6c-e3d4-4bed-9368-56d511882835-integrated'}}}


    100   278  100   215    0    63      1      0  0:03:35  0:02:34  0:01:01    50

