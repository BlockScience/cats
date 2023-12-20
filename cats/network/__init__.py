import json
import os
import subprocess
from copy import copy, deepcopy

import ipfsapi as ipfsApi
from cats.network.aws import s3_client
from cats.network.cod import CoD


class MeshClient(CoD):
    def __init__(self, ipfsClient, filecoinClient=None, awsClient=None):
        self.ipfsClient = ipfsClient
        self.filecoinClient = filecoinClient
        self.awsClient = awsClient
        self.context = ...
        CoD.__init__(self)

    # def getInvoice(self, invoiceCID: str):
    #     return self.getObjs(invoiceCID)
    #
    # def getOrder(self, orderCID: str):
    #     return self.getObjs(orderCID)
    #
    # def getInvoicesCID(self, orderCID: str):
    #     order =  self.getOrder(orderCID)
    #     return order.invoicesCID
    #
    # def getOrderCID(self, invoiceCID: str):
    #     invoice =  self.getInvoice(invoiceCID)
    #     return invoice.orderCID
    #
    # def getFunctionCID(self, orderCID: str):
    #     order =  self.getOrder(orderCID)
    #     return order.functionCID
    #
    # def getStructureCID(self, orderCID: str):
    #     order =  self.getOrder(orderCID)
    #     return order.structureCID

    def initBOMjson(self, structure_cid: str, function_cid: str, data_cid: str, seed_cid=None):
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

        init_invoice_cid = self.ipfsClient.add_json(init_invoice)
        init_order['invoice_cid'] = init_invoice_cid
        init_order_cid = self.ipfsClient.add_json(init_order)

        invoice = copy(init_invoice)
        invoice['order_cid'] = init_order_cid
        invoice_cid = self.ipfsClient.add_json(invoice)


        init_bom = {
            'invoice_cid': invoice_cid,
            'log_cid': None,
        }
        init_bom_json_cid = self.ipfsClient.add_json(init_bom)
        return init_bom_json_cid

    def initBOMcar(self, structure_cid: str, function_cid: str, data_cid: str, init_bom_filename: str, seed_cid=None):
        init_bom_json_cid = self.initBOMjson(structure_cid, function_cid, data_cid)
        car_bom_cid, init_bom_json_cid = self.convertBOMtoCAR(init_bom_json_cid, init_bom_filename)
        return car_bom_cid, init_bom_json_cid

    def get(self, cid: str, filepath: str):
        subprocess.check_output(
            f"ipfs get {cid}",
            stderr=subprocess.STDOUT,
            shell=True
        )
        os.rename(cid, filepath)

    def cat(self, cid: str):
        return subprocess.check_output(['ipfs', 'cat', cid]).decode()

    def getCar(self, cid: str, filepath: str):
        subprocess.check_output(
            f"ipfs dag export {cid} > {filepath}",
            stderr=subprocess.STDOUT,
            shell=True
        )

    def getBom(self, cid: str, filepath: str):
        self.get(cid, filepath)
        bom = dict(json.loads(filepath))
        subprocess.check_output(
            f"rm {filepath}",
            stderr=subprocess.STDOUT,
            shell=True
        )
        return bom

    def transfer_bom_to_w3(self, bom_cid: str, filepath: str):
        self.getCar(bom_cid, filepath)
        storage_bom_cid = self.ipfsClient.post_upload(filepath)
        return storage_bom_cid, bom_cid

    def convertBOMtoCAR(self, bom_cid: str, filepath: str):
        self.getCar(bom_cid, filepath)
        car_bom_cid = None
        try:
            car_bom_cid = self.ipfsClient.add(filepath)['Hash']
        except:
            for attrs in self.ipfsClient.add(filepath):
                if attrs['Name'] == filepath:
                    print(attrs)
                    car_bom_cid = attrs['Hash']
        return car_bom_cid, bom_cid

    def getEnhancedBom(self, bom_json_cid: str):
        self.get(bom_json_cid, 'bom.json')
        bom = json.loads(open('bom.json', 'r').read())
        enhanced_bom = deepcopy(bom)
        enhanced_bom['bom_json_cid'] = bom_json_cid

        self.get(bom['invoice_cid'], 'invoice.json')
        enhanced_bom['invoice'] = json.loads(open('invoice.json', 'r').read())

        self.get(enhanced_bom['invoice']['order_cid'], 'order.json')
        enhanced_bom['order'] = json.loads(open('order.json', 'r').read())

        self.get(
            enhanced_bom['order']['structure_cid']['Hash'],
            enhanced_bom['order']['structure_cid']['Name']
        )
        return enhanced_bom, bom

    def createInvoice(self, orderCID: str, dataCID: str, seedCID: str):
        invoice = {'orderCID': orderCID, 'dataCID': dataCID, 'seedCID': seedCID}
        invoice_cid = self.ipfsClient.add_json(invoice)
        return invoice_cid



# class NetworkClient(CoD):
#     def __init__(self,
#         bomURI: str
#     ):
#         self.ipfsStorageClient = MeshClient(storageClient)
#         self.codClient = CoD()
#         bomURIpath = Path(bomURI)
#         if bomURIpath.exists() is False and s3_client.s3ObjExist(bomURI) is True:
#             self.bomURI = None
#             self.bomCID = self.ipfsStorageClient.cid(bomURI)
#         elif bomURIpath.exists() is False and s3_client.s3ObjExist(bomURI) is True:
#             self.bomURI = bomURI
#             self.bomCID = self.ipfsStorageClient.cid(bomURI)