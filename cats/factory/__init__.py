import json
from copy import deepcopy

from cats.executor import Executor
from cats.service import Service


class Factory:
    def __init__(self,
        service: Service,
        order=None
    ):
        self.Executor = Executor(service=service)
        self.order = order

    def initCAT(self,
        function_cid, ipfs_uri,
        structure_cid=None, structure_filepath=None
    ):
        return self.service.initBOMcar(
            structure_cid=structure_cid,
            structure_filepath=structure_filepath,
            function_cid=function_cid,
            init_data_cid=ipfs_uri
        )

    def execute(self):
        enhanced_bom, _ = self.Executor.execute()
        return enhanced_bom





