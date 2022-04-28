import subprocess, time, json

from pycats import CATS_HOME


class IPFS():
    def __init__(self,
        DRIVER_IPFS_DIR=f'{CATS_HOME}/cadStore'
    ):
        self.DRIVER_IPFS_DIR = DRIVER_IPFS_DIR
        self.ipfs_daemon_cmd = 'ipfs daemon'
        self.daemon_proc = None
        self.daemon_pid = None
        self.ipfs_id = None
        self.ipfs_addresses = None
        self.ip4_tcp_addresses = None

    def start_daemon(self):
        self.daemon_proc = subprocess.Popen(
            self.ipfs_daemon_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        self.daemon_pid = self.daemon_proc.pid
        time.sleep(15)
        ipfs_id_cmd = f'ipfs id > {self.DRIVER_IPFS_DIR}/ipfs_id.json'
        output = subprocess.check_output(ipfs_id_cmd, shell=True)
        self.ipfs_id = open(f'{self.DRIVER_IPFS_DIR}/ipfs_id.json') # ToDO: change from file
        self.ipfs_addresses = json.load(self.ipfs_id)["Addresses"]
        self.ip4_tcp_addresses = [
            x for x in self.ipfs_addresses if ('tcp' in x) and ('ip4' in x) and ('127.0.0.1' not in x) and ('172.17.0.3' not in x)
        ]

        return self

    def ipfs_swarm_connect(self, addresses):
        for address in addresses:
            output = subprocess.check_output(f"ipfs swarm connect {address}", shell=True) \
                .decode('ascii').replace('\n', '').split(' ')
            if output[2] == 'success':
                return address
            else:
                return None

    def ipfs_add(self, file):
        ipfs_add = f'ipfs add {file}'.split(' ')
        [ipfs_action, cid, file_name] = subprocess.check_output(ipfs_add) \
            .decode('ascii').replace('\n', '').split(' ')
        return ipfs_action, cid, file_name
