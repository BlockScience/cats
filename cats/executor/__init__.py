# from cats.io.input.structure import Structure
# from cats.io.input.function import Function
# from cats.io.input.order import Order
# from cats.io.output import Invoice
from cats.io.input.structure import Structure
from cats.io.input.function import Function
from cats.service import Service


class Executor(Structure):
    def __init__(self,
        service: Service
    ):
        self.service: Service = service
        self.structure: Structure = Structure(self.service)
        self.function: Function = Function(self.service)
        self.bom_json_cid: str = self.service.bom_json_cid
        self.enhanced_bom: dict = None
        self.orderCID = None
        self.invoiceCID = None
        self.job_id = None


        # self.order = None
        # self.structure: Structure = self.order.structure
        # self.function: Function = self.order.function
        # ...

    # def execute(self):
    #     self.structure.deploy(self.function)
    #     invoice = ...
    #
    #     self.response['invoiceCID'] = invoice.invoiceCID
    #     self.response['orderCID'] = invoice.orderCID
    #     self.response['dataCID'] = invoice.dataCID
    #     self.response['seedCID'] = invoice.seedCID
    #     # ToDo: BOM
    #     return self.response


    def generateInvoice(self, order_cid):
        ...
        return self.invoiceCID


    def execute(self):
        self.enhanced_bom, bom = self.structure.deploy()
        self.orderCID = self.enhanced_bom['invoice']['order_cid']
        self.invoiceCID = self.enhanced_bom['invoice_cid']

        self.job_id = self.function.execute()
        self.enhanced_bom['job_id'] = self.job_id
        return self.enhanced_bom, bom
        # return self.invoiceCID

    # def deploy(self, function: Function):
    #     self.exe_response = function.deploy()
    #     return self.exe_response
