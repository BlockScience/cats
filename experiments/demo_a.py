from dag_json import decode, encode
from multiformats import CID
import ipfsApi
api = ipfsApi.Client('127.0.0.1', 5001)

encoded_order = encode({
    'order_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
    'invoice_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
    'function_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp'),
    'structure_cid': CID.decode('QmUGhP2X8xo9dsj45vqx1H6i5WqPqLqmLQsHTTxd3ke8mp')
})

help(encoded_order)

# def encode_init_invoice(data_cid: str):
#     encoded_init_invoice = encode({
#         'order_cid': None,
#         'data_cid': data_cid,
#         'seed_cid': None,
#     })
#     encoded_init_invoice.
#     init_invoice_cid = encoded_cid(encoded_init_invoice)
#     encoded_init_invoice = repr(decode(encoded_init_invoice))
#     encoded_init_invoice['invoice_cid']


# encoded_init_invoice =  encode_init_invoice('')
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