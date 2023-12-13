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
apikey = os.getenv('VYDEVICE_APIKEY')
port = os.getenv('VYDEVICE_PORT')
protocol = os.getenv('VYDEVICE_PROTOCOL')
verify = os.getenv('VYDEVICE_VERIFY_SSL')
if verify == "False":
    verify = False
else:
    verify = True


class TestVyDevice(unittest.TestCase):
    def setUp(self):
        self.device = VyDevice(hostname=hostname, apikey=apikey, port=port, protocol=protocol, verify=verify)

    def test_001_retrieve_show_config(self):
        response = self.device.retrieve_show_config(['system'])
        pprint.pprint(response)

        self.assertEqual(response.status, 200)
        self.assertIsNotNone(response.result)
        self.assertFalse(response.error)

    def test_010_configure_set_interface(self):
        response = self.device.configure_set(path=["interfaces", "dummy", "dum1", "address", "192.168.140.1/24"])
        #pprint.pprint(response)

        self.assertEqual(response.status, 200)
        self.assertIsNone(response.result)
        self.assertFalse(response.error)
        

    def test_011_configure_delete_interface(self):
        response = self.device.configure_delete(path=["interfaces", "dummy", "dum1"])
        pprint.pprint(response)
        
        self.assertEqual(response.status, 200)
        self.assertIsNone(response.result)
        self.assertFalse(response.error)        


    def test_300_config_file_save(self):
        response = self.device.config_file_save(file="/config/test300.config")
        pprint.pprint(response)

        self.assertEqual(response.status, 200)
        self.assertIsNotNone(response.result)
        self.assertFalse(response.error)

    def test_301_config_file_save(self):
        response = self.device.config_file_save()
        pprint.pprint(response)

        self.assertEqual(response.status, 200)
        self.assertIsNotNone(response.result)
        self.assertFalse(response.error)


    def test_302_config_file_load(self):
        response = self.device.config_file_load(file="/config/test300.config")
        pprint.pprint(response)

        self.assertEqual(response.status, 200)
        self.assertIsNone(response.result)
        self.assertFalse(response.error)




    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()

