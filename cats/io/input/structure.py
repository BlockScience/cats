# from cats.io.input import Function
from pprint import pprint

import cats
from cats.service import Service
from python_terraform import Terraform


class Plant:
    def __init__(self,
        deployment
    ):
        self.deployment = deployment
        self.dep_response: dict = {}
        self.exe_response: dict = {}

    def deploy(self, deployment=None):
        if deployment is not None:
            self.deployment = deployment
        self.dep_response = self.deployment.deploy()
        return self.dep_response


class InfraStructure:
    def __init__(self,
        deployment
    ):
        self.deployment = deployment
        self.response: dict = {}

    def deploy(self, deployment=None):
        if deployment is not None:
            self.deployment = deployment
        self.response = self.deployment.deploy()
        return self.response


class Structure:
    def __init__(self,
        # plant: Plant = None,
        # infraStructure: InfraStructure = None,
        service: Service = None
    ):
        # self.plant: Plant = plant
        self.service: Service = service
        self.bom_json_cid = self.service.bom_json_cid
        # self.infraStructure: Terraform = Terraform(working_dir=cats.CWD)

    def deploy(self):
        print()
        print()
        print('Destroy Structure!')
        self.service.executeCMD(['terraform', 'destroy', '--auto-approve'])
        print()
        print()
        print('Initialize Structure!')
        self.service.executeCMD(['terraform', 'init', '--upgrade']) # self.service.executeCMD(['terraform', 'plan'])
        print()
        print()
        print('Deploy Structure!')
        self.service.executeCMD(['terraform', 'apply', '--auto-approve'])