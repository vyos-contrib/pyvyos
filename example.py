#import warnings
#warnings.filterwarnings("ignore", category=RuntimeWarning)    

import sys
import os

# Adicione o diretório raiz do projeto ao sys.path para que possa importar vyapi
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))


import unittest
from vyapi.device import VyDevice
from vyapi.device import ApiResponse
from dotenv import load_dotenv
import pprint 

load_dotenv()  

hostname = os.getenv('VYDEVICE_HOSTNAME')
key = os.getenv('VYDEVICE_KEY')
port = os.getenv('VYDEVICE_PORT')
protocol = os.getenv('VYDEVICE_PROTOCOL')
verify = os.getenv('VYDEVICE_VERIFY_SSL')
if verify == "False":
    verify = False

else:
    verify = True

if __name__ == '__main__':
    device = VyDevice(hostname=hostname, key=key, port=port, protocol=protocol, verify=verify)
    response = device.retrieve_show_config(['system'])
    pprint.pprint(response)

