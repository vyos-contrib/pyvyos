import sys
import os
import unittest
from vyapi.device import VyDevice
from vyapi.device import ApiResponse
from dotenv import load_dotenv
import os
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



class TestVyDevice(unittest.TestCase):
    def setUp(self):
        self.device = VyDevice(hostname=hostname, key=key, port=port, protocol=protocol, verify=verify)

    def test_show_configuration_content(self):
        response = self.device.retrieve_show_config(['system'])

        self.assertEqual(response.status, 200)
        self.assertIsNotNone(response.result)
        self.assertFalse(response.error)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

