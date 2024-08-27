# importing modules
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
import sys
import os
# adding pyvyos to sys.path
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

import unittest
from dotenv import load_dotenv
import pprint
import random
import string

# importing pyvyos modules
from pyvyos.device import VyDevice
from pyvyos.device import ApiResponse


# getting env variables
load_dotenv()
hostname = os.getenv('VYDEVICE_HOSTNAME')
apikey = os.getenv('VYDEVICE_APIKEY')
port = os.getenv('VYDEVICE_PORT')
protocol = os.getenv('VYDEVICE_PROTOCOL')
verify = os.getenv('VYDEVICE_VERIFY_SSL')
if verify == "False":
    verify = False
else:
    verify = True

# running example
if __name__ == '__main__':
    # preparing connection to vyos device
    device = VyDevice(hostname=hostname, apikey=apikey, port=port, protocol=protocol, verify=verify)



    #response = device.retrieve_show_config(['system'])
    #pprint.pprint(response)

    #print("### Generating ssh key ###")
    #randstring = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
    #keyrand =  f'/tmp/key_{randstring}'
    #response = device.generate(path=["ssh", "client-key", keyrand])
    #pprint.pprint(response)



    #response = device.retrieve_return_values(path=["interfaces", "ethernet", "eth0", "address"])
    #pprint.pprint(response)

    #response = device.reset(path=["conntrack-sync", "internal-cache"])
    #pprint.pprint(response)

    #response = device.reboot(path=["now"])
    #pprint.pprint(response)

    #response = device.shutdown(path=["now"])
    #pprint.pprint(response)

    #response = device.image_add(url="https://github.com/vyos/vyos-rolling-nightly-builds/releases/download/1.5-rolling-202312130023/vyos-1.5-rolling-202312130023-amd64.iso")
    #pprint.pprint(response)

    response = device.image_delete(name="foo")
    pprint.pprint(response)
