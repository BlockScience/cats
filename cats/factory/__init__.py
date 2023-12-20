import json

from cats.executor import Executor
# from cats.io.input.order import Order


# from cats.utils import Dict2Class
# from cats.network import MeshClient, NetworkClient


class Factory:
    def __init__(self,
        order: json
    ):
        self.orderJSON = order
        self.orderDict = order.__dict__
        # self.order: Order = Order(
        #     orderCID=self.orderDict['orderCID'],
        #     invoicesCID=self.orderDict['invoicesCID'],
        #     functionCID=self.orderDict['functionCID'],
        #     structureCID=self.orderDict['structureCID'],
        #     netClient=NetworkClient()
        # )

        return Executor(self.orderDict)