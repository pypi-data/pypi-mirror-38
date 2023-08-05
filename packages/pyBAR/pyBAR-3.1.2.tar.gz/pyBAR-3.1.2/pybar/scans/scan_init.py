import logging

from pybar.fei4_run_base import Fei4RunBase
from pybar.run_manager import RunManager


class InitScan(Fei4RunBase):
    '''Init scan
    '''
    _default_run_conf = {
        "broadcast_commands": False,
        "threaded_scan": False
    }

    def configure(self):
        pass

    def scan(self):
        pass

    def analyze(self):
        pass


if __name__ == "__main__":
    with RunManager('configuration.yaml') as runmngr:
        runmngr.run_run(InitScan)
