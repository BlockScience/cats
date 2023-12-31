```python
import json
from pprint import pprint

from cats.network import ipfsApi, MeshClient
from cats.service import Service
from process import *
```

    /home/jjodesty/Projects/Research/cats-research/cats/network/__init__.py:6: FutureWarning: The `ipfsapi` library is deprecated and will stop receiving updates on the 31.12.2019! If you are on Python 3.5+ please enable and fix all Python deprecation warnings (CPython flag `-Wd`) and switch to the new `ipfshttpclient` library name. Python 2.7 and 3.4 will not be supported by the new library, so please upgrade.
      import ipfsapi as ipfsApi
    /home/jjodesty/Projects/Research/cats-research/venv/lib/python3.10/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
      from .autonotebook import tqdm as notebook_tqdm
    2023-12-31 16:19:26,571	INFO util.py:159 -- Missing packages: ['ipywidgets']. Run `pip install -U ipywidgets`, then restart the notebook server for rich notebook output.



```python
service = Service(
    meshClient=MeshClient(
        ipfsClient=ipfsApi.Client('127.0.0.1', 5001)
    )
)
```


```python
order_bom_0 = service.create_order(
    process_obj=process_0,
    data_dirpath='data',
    structure_filepath='main.tf',
    endpoint='http://127.0.0.1:5000/cat/node/preproc'
)

```


```python
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
```


```python
cat_0 = order_bom_0, invoice_bom_0, modified_catJob_0 = service.cat_repl(
    order_bom=order_bom_0,
    bom_function=modify_bom
)
```

    {'function': {'infrafunction_cid': None,
                  'process_cid': 'QmXqKpSVBuoZD2QG8hT3tTF8ai6cHV8iTHt2tF5sM3scmc'},
     'invoice': {'data_cid': 'QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN'},
     'order': {'endpoint': 'http://127.0.0.1:5000/cat/node/preproc',
               'function_cid': 'QmPMniqGmZ28QnDwa2UJqkcWjkkaehkEKcXD47kLUVWaEd',
               'structure_cid': 'QmXQjsVw8JPqacrtLLUTWnCrkm8xHn1Zoc7Z5wmU8C6dkh',
               'structure_filepath': 'main.tf'}}
    curl -X POST -H "Content-Type: application/json" -d \
    '{
        "invoice": {
            "data_cid": "QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN"
        },
        "order": {
            "function_cid": "QmPMniqGmZ28QnDwa2UJqkcWjkkaehkEKcXD47kLUVWaEd",
            "structure_cid": "QmXQjsVw8JPqacrtLLUTWnCrkm8xHn1Zoc7Z5wmU8C6dkh",
            "structure_filepath": "main.tf",
            "endpoint": "http://127.0.0.1:5000/cat/node/preproc"
        },
        "function": {
            "process_cid": "QmXqKpSVBuoZD2QG8hT3tTF8ai6cHV8iTHt2tF5sM3scmc",
            "infrafunction_cid": null
        }
    }' http://127.0.0.1:5000/cat/node/preproc


      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    100  1503  100  1091  100   412     11      4  0:01:43  0:01:33  0:00:10   271



```python
pprint(order_bom_0)
```

    {'function': {'infrafunction_cid': None,
                  'process_cid': 'QmXqKpSVBuoZD2QG8hT3tTF8ai6cHV8iTHt2tF5sM3scmc'},
     'invoice': {'data_cid': 'QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN'},
     'order': {'endpoint': 'http://127.0.0.1:5000/cat/node/preproc',
               'function_cid': 'QmPMniqGmZ28QnDwa2UJqkcWjkkaehkEKcXD47kLUVWaEd',
               'structure_cid': 'QmXQjsVw8JPqacrtLLUTWnCrkm8xHn1Zoc7Z5wmU8C6dkh',
               'structure_filepath': 'main.tf'}}



```python
pprint(invoice_bom_0)
```

    {'POST': 'curl -X POST -H "Content-Type: application/json" -d \'{"invoice": '
             '{"data_cid": "QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN"}, '
             '"order": {"function_cid": '
             '"QmPMniqGmZ28QnDwa2UJqkcWjkkaehkEKcXD47kLUVWaEd", "structure_cid": '
             '"QmXQjsVw8JPqacrtLLUTWnCrkm8xHn1Zoc7Z5wmU8C6dkh", '
             '"structure_filepath": "main.tf", "endpoint": '
             '"http://127.0.0.1:5000/cat/node/preproc"}, "function": '
             '{"process_cid": "QmXqKpSVBuoZD2QG8hT3tTF8ai6cHV8iTHt2tF5sM3scmc", '
             '"infrafunction_cid": null}}\' http://127.0.0.1:5000/cat/node/preproc',
     'bom_json_cid': 'QmPtVQGPkQtnPSTkCsT5itV4W2ProZLcz5XFbJP383x4vg',
     'function': {'infrafunction_cid': None,
                  'process_cid': 'QmXqKpSVBuoZD2QG8hT3tTF8ai6cHV8iTHt2tF5sM3scmc'},
     'init_data_cid': 'ipfs://QmQpyDtFsz2JLNTSrPRzLs1tzPrfBxYbCw6kehVWqUXLVN/*csv',
     'invoice': {'data_cid': 'QmdNH4dewfpaRvRef88A8fcHVwaKFa4MiVt2LBxedovEnk',
                 'order_cid': 'QmSdphNtobJUSiMqELp5HmxsbQEkQs65J1wEvfvanr2d9a',
                 'seed_cid': None},
     'invoice_cid': 'QmbXDsxHmNJmoNNtaUKtA1nwoRp54oDbGeoXNfqY6vXPqZ',
     'log': {'egress_job_id': '96f0d71f-b26c-4dc6-b6f6-254377e5815b',
             'ingress_job_id': '391b5e20-dd59-4ce2-8fe9-e45f5bfae276',
             'integration_output': 's3://catstore3/boms/result-20231231-391b5e20-dd59-4ce2-8fe9-e45f5bfae276-integrated'},
     'log_cid': 'QmUt62xBUUp7awPFP5mBQqMgbFC8Z7becYzkLtQrtEYuSA',
     'order': {'function_cid': 'QmPMniqGmZ28QnDwa2UJqkcWjkkaehkEKcXD47kLUVWaEd',
               'invoice_cid': 'QmRWL4HD43wQYk3cfc9ywt9JDEoA18p5CX3AZo2pYTC1aM',
               'structure_cid': 'QmXQjsVw8JPqacrtLLUTWnCrkm8xHn1Zoc7Z5wmU8C6dkh',
               'structure_filepath': 'main.tf'}}



```python
cat_1 = order_bom_1, invoice_bom_1, modified_catJob_1 = modified_catJob_0(
    process_obj=process_1
)
```

      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

    curl -X POST -H "Content-Type: application/json" -d \
    '{
        "order": {
            "function_cid": "QmZCdhBAvgenFaKUQpjz4G62TtMoLCJgcsMhA799StxzsT",
            "structure_cid": "QmXQjsVw8JPqacrtLLUTWnCrkm8xHn1Zoc7Z5wmU8C6dkh",
            "structure_filepath": "main.tf",
            "endpoint": "http://127.0.0.1:5000/cat/node/postproc"
        },
        "invoice": {
            "data_cid": "QmdNH4dewfpaRvRef88A8fcHVwaKFa4MiVt2LBxedovEnk"
        },
        "function": {
            "infrafunction_cid": null,
            "process_cid": "QmXC2XLDePUxCoPtETPejd5uwF3BcaoQNAn2vRU4a4BK7z"
        }
    }' http://127.0.0.1:5000/cat/node/postproc


    100  1504  100  1091  100   413     11      4  0:01:43  0:01:36  0:00:07   258



```python
pprint(order_bom_1)
```

    {'function': {'infrafunction_cid': None,
                  'process_cid': 'QmXC2XLDePUxCoPtETPejd5uwF3BcaoQNAn2vRU4a4BK7z'},
     'invoice': {'data_cid': 'QmdNH4dewfpaRvRef88A8fcHVwaKFa4MiVt2LBxedovEnk'},
     'order': {'endpoint': 'http://127.0.0.1:5000/cat/node/postproc',
               'function_cid': 'QmZCdhBAvgenFaKUQpjz4G62TtMoLCJgcsMhA799StxzsT',
               'structure_cid': 'QmXQjsVw8JPqacrtLLUTWnCrkm8xHn1Zoc7Z5wmU8C6dkh',
               'structure_filepath': 'main.tf'}}



```python
pprint(invoice_bom_1)
```

    {'POST': 'curl -X POST -H "Content-Type: application/json" -d \'{"order": '
             '{"function_cid": "QmZCdhBAvgenFaKUQpjz4G62TtMoLCJgcsMhA799StxzsT", '
             '"structure_cid": "QmXQjsVw8JPqacrtLLUTWnCrkm8xHn1Zoc7Z5wmU8C6dkh", '
             '"structure_filepath": "main.tf", "endpoint": '
             '"http://127.0.0.1:5000/cat/node/postproc"}, "invoice": {"data_cid": '
             '"QmdNH4dewfpaRvRef88A8fcHVwaKFa4MiVt2LBxedovEnk"}, "function": '
             '{"infrafunction_cid": null, "process_cid": '
             '"QmXC2XLDePUxCoPtETPejd5uwF3BcaoQNAn2vRU4a4BK7z"}}\' '
             'http://127.0.0.1:5000/cat/node/postproc',
     'bom_json_cid': 'QmRu1KSrCQL7SLG2Yisac8brty2n3dDi3YakdiouAZhRxL',
     'function': {'infrafunction_cid': None,
                  'process_cid': 'QmXC2XLDePUxCoPtETPejd5uwF3BcaoQNAn2vRU4a4BK7z'},
     'init_data_cid': 'ipfs://QmWST1g3CCKwbWzBR3McziuBF3C8JMevJzm2i6zq95oJEX/*csv',
     'invoice': {'data_cid': 'QmP7NkFK44nhEYGhvkk1XaWG2DzRXQG2xCAqRVUf2KrmE6',
                 'order_cid': 'Qma91qb8Ht9J62dLTLNCDDfos1mJ9CbSPcJnYmfXPmzhQ6',
                 'seed_cid': None},
     'invoice_cid': 'QmNYEVWNeEEwsBYcs4TE1xvLhvC26fJHzRCbsLEkadx3af',
     'log': {'egress_job_id': '8749b04c-3245-4c57-971d-0f46040055d4',
             'ingress_job_id': '03b4d888-6120-4b72-a4c4-70869f89ccf2',
             'integration_output': 's3://catstore3/boms/result-20231231-03b4d888-6120-4b72-a4c4-70869f89ccf2-integrated'},
     'log_cid': 'QmVexzCQUWP3NVwQUspYCGhFZKVKVN42pDwXY3HEw5n1i8',
     'order': {'function_cid': 'QmZCdhBAvgenFaKUQpjz4G62TtMoLCJgcsMhA799StxzsT',
               'invoice_cid': 'QmRWL4HD43wQYk3cfc9ywt9JDEoA18p5CX3AZo2pYTC1aM',
               'structure_cid': 'QmXQjsVw8JPqacrtLLUTWnCrkm8xHn1Zoc7Z5wmU8C6dkh',
               'structure_filepath': 'main.tf'}}



```python

```
