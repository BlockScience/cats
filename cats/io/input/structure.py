from cats.service import Service


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
        service: Service = None
    ):
        self.service: Service = service
        self.bom_json_cid = self.service.bom_json_cid
        # self.plant: Plant = plant
        # self.infraStructure: Terraform = Terraform(working_dir=cats.CWD)

    def destroy(self):
        print('Destroy Structure!')
        self.service.executeCMD(['terraform', 'destroy', '--auto-approve'])
        print()
        print()

    def initialize(self):
        print('Initialize Structure!')
        self.service.executeCMD(['terraform', 'init', '--upgrade'])  # self.service.executeCMD(['terraform', 'plan'])
        print()
        print()

    def apply(self):
        print('Apply Structure!')
        self.service.executeCMD(['terraform', 'apply', '--auto-approve'])
        print()
        print()

    def redeploy(self):
        print()
        print()
        print('Deploy Structure!')
        self.destroy()
        self.initialize()
        self.apply()
        