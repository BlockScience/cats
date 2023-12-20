

# ToDo: create order locally and remotely and get all paths under the condition that the exist already
# from pathlib import Path
#
# from cats.network import NetworkClient


# class BOM:
#     def __init__(self, netClient: NetworkClient):
#         self.netClient: NetworkClient = netClient
#         self.bomURI = self.netClient.bomURI
#         self.bomCID = self.netClient.bomCID
#
#         self.invoiceURI: str = None
#         self.logURI: str = None
#
#         self.invoiceCID: str = invoiceCID
#         self.logCID: str = logCID


# class Invoice:
#     @dispatch(str, str, str)
#     def __init__(self,
#         orderCID: str,
#         dataCID: str,
#         seedCID: str = None,
#         invoiceCID: str = None
#     ):
#         self.netClient: NetworkClient = None
#
#         self.invoiceURI: str = None
#         self.orderURI: str = None
#         self.dataURI: str = None
#         self.seedURI: str = None
#
#         self.invoiceCID: str = invoiceCID
#         self.orderCID: str = orderCID
#         self.dataCID: str = dataCID
#         self.seedCID: str = seedCID
#
#     @dispatch(NetworkClient, str)
#     def __init__(self,
#         invoiceURI: str,
#         netClient: NetworkClient = None
#     ):
#         self.netClient: NetworkClient = netClient
#
#         invoiceURIpath = Path(invoiceURI)
#         if Path.exists(invoiceURIpath) is False and self.netClient.s3ObjExist(invoiceURI) is True:
#             self.invoiceURI: str = invoiceURI,
#             self.orderURI: str = invoiceURI+'/orderURI', # use boto3 and self.orderURI
#             self.dataURI: str = invoiceURI+'/dataURI' # use boto3 and self.orderURI
#         else:
#             self.invoiceURI: str = invoiceURIpath.__str__()
#             self.orderURI: str = str(invoiceURIpath / 'orderURI')
#             self.dataURI: str = str(invoiceURIpath / 'dataURI')
#
#         self.invoiceCID: str = self.netClient.cid(self.invoiceURI), # CoD Ingress (Plant)
#         self.orderCID: str = self.netClient.getObj(self.invoiceCID) # MeshClient request
#         self.dataCID: str = self.netClient.getObj(self.invoiceCID) # MeshClient request, # IPFS Client (whatever is lighter): get cid or re-cid
#
#     # s3Utils.get_s3_bucket_prefix_pair()