from typing import Any


class ipfsStrorage:
    def __init__(self, client):
        # self.storageClient = storageClient
        self.client = client

    def ser(self, obj: Any): Path = ...

    def cidWrite(self, source: str, dest: str): str = ...

    def cidWriteObj(self, obj: Any, dest: str): str = ...

    def getObj(self, cid: str): str = ...

    def getObjs(self, cid: str): str = ...
