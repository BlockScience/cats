from cats.io.input.function import InfraFunction, Processor
from cats.service import Service


class Function(InfraFunction):
    def __init__(self,
        service: Service
    ):
        self.service: Service = service
        self.infraFunc = InfraFunction.__init__(self, self.service)
        self.orderCID: str = self.service.orderCID
        self.processCID = self.service.processCID
        self.process: Processor = None
        self.dataCID: str = None
        self.invoiceCID: str = None

    def execute(self):
        self.process = self.infraFunc.configureProcess()
        self.dataCID = self.process.execute(self.processCID)
        self.invoiceCID = self.service.createInvoice(self.orderCID, self.dataCID, self.service.seedCID)
        return self.invoiceCID

