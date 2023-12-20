## Tested Requirement:
# from pathlib import Path

# from cats.io.input.function import Function
# from cats.io.input.invoices import Invoices
# from cats.io.input.structure import Structure
# # from cats.io.output import Invoice
# from cats.network import NetworkClient

# class Order:
#     @dispatch(NetworkClient, str, set[str], str, str)
#     def __init__(self,
#         orderCID: str,
#         invoicesCID: str,
#         functionCID: str,
#         structureCID: str,
#         netClient: NetworkClient = None,
#     ):
#         self.netClient: NetworkClient = netClient
#
#         self.orderURI: str = None
#         self.functionURI: str = None
#         self.structureURI: str = None
#         self.invoicesURI: str = None
#
#         self.orderPath: str = None
#         self.functionPath: str = None
#         self.structurePath: str = None
#         self.invoicesPath: str = None
#
#         self.orderCID: str = orderCID
#         self.invoicesCID: str = invoicesCID
#         self.functionCID: str = functionCID
#         self.structureCID: str = structureCID
#
#         # ToDO: invoices here may just be CIDs
#         # self.invoices: set[Invoice] = self.netClient.getInvoices(self.invoicesCID) # CoD Ingress (Plant)
#         self.invoices: Invoices = self.netClient.getInvoices(self.invoicesCID)
#         self.function: Function = self.netClient.getObj(self.functionCID)  # MeshClient Ingest
#         self.structure: Structure = self.netClient.getObj(self.structureCID)  # MeshClient Ingest
#         # self.invoices: Invoices = Invoices(self.invoicesCID)
#         # self.function: Function = Function(self.functionCID) # MeshClient Ingest
#         # self.structure: Structure = Structure(self.structureCID) # MeshClient Ingest
#
#     # ToDo: create order locally and remotely and get all paths under the condition that the exist already
#     @dispatch(NetworkClient, str)
#     def __init__(self,
#         netClient: NetworkClient,
#         orderURI: str = None,
#         functionURI: str = None,
#         structureURI: str = None,
#         invoicesURI: str = None
#     ):
#         self.netClient: NetworkClient = netClient
#
#         orderURIpath = Path(orderURI) # use boto3 and self.orderURI
#         if Path.exists(orderURIpath) is False and self.netClient.s3ObjExist(orderURI) is True:
#             self.orderURI: str = orderURI
#             self.functionURI: str = orderURI+'/functionURI',
#             self.structureURI: str = orderURI+'/structureURI',
#             self.invoicesURI: str = orderURI+'/invoicesURI',
#             self.orderCID: str = self.netClient.cid(self.orderURI) # CoD Migration
#         else:
#             self.orderURI: str = orderURIpath.__str__()
#             self.functionURI: str = str(orderURIpath / "functionURI")
#             self.structureURI: str = str(orderURIpath / "structureURI")
#             self.invoicesURI: str = str(orderURIpath / "invoicesURI")
#             self.orderCID: str = self.netClient.cid(self.orderURI) # CoD Ingress w/ pre-migration step (Plant Config for reformating / reparts)
#
#         self.invoicesCID: str = self.netClient.getInvoicesCID(self.orderCID),  # MeshClient request
#         self.functionCID: str = self.netClient.getFunctionCID(self.orderCID),  # MeshClient request
#         self.structureCID: str = self.netClient.getStructureCID(self.orderCID),  # MeshClient request
#
#         self.invoices: set[Invoice] = self.netClient.getInvoices(self.invoicesCID) # CoD Ingress (Plant)
#         self.function: Function = self.netClient.getObj(self.functionCID) # MeshClient Ingest
#         self.structure: Structure = self.netClient.getObj(self.structureCID) # MeshClient Ingest
#
#     # ToDo: addFunction and addStructure Methods
#     @dispatch(Invoice)
#     def addInvoice(self, invoice: Invoice):
#         self.invoices = self.invoices + set[invoice]
#         self.invoicesCIDs = self.invoicesCIDs + set[self.netClient.cid(invoice)]
#
#     @dispatch(str)
#     def addInvoice(self, invoiceCID: str):
#         self.invoices = self.invoices + set[self.getInvoice(invoiceCID)]
#         self.invoicesCIDs = self.invoicesCIDs + set[invoiceCID]
#
#     @dispatch(set[Invoice])
#     def addInvoices(self, invoices: set[Invoice]):
#         self.invoices = self.invoices + invoices
#         self.invoicesCIDs = self.invoicesCIDs + set(map(lambda i: i.invoiceCID,  invoices))
#
#     @dispatch(set[str])
#     def addInvoices(self, invoiceCIDs: set[str]):
#         self.invoices = self.invoices + set(map(lambda cid: self.getInvoice(cid),  invoiceCIDs))
#         self.invoicesCIDs = self.invoicesCIDs + invoiceCIDs