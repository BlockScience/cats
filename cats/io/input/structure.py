from cats.service import Service


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
