import urllib3
urllib3.disable_warnings()

import requests
import json
import pprint
from dataclasses import dataclass

@dataclass
class ApiResponse:
    status: int
    request: dict
    result: dict
    error: str
    
class VyDevice:
    def __init__(self, hostname, key, protocol='https', port=443, verify=True, timeout=10):
        self.hostname = hostname
        self.key = key
        self.protocol = protocol
        self.port = port
        self.verify = verify
        self.timeout = timeout


    def _get_url(self, command):
        return f"{self.protocol}://{self.hostname}:{self.port}/{command}"

    def _get_payload(self, op, path):
        return {
            'data': json.dumps({'op': op, 'path': path}),
            'key': self.key
        }

    def _api_request(self, command, op, path=[], method='POST'):
        url = self._get_url(command)
        payload = self._get_payload(op, path)

        
        headers = {}
        error = False      
        result = {}

        try:
            resp = requests.post(url, verify=self.verify, data=payload, timeout=self.timeout, headers=headers)
        
            if resp.status_code == 200:
                try:
                    resp_decoded = resp.json()
                    if resp_decoded['success'] == True:
                        result = resp_decoded['data']
                        error = False
                    else:   
                        error = resp_decoded['error']
                   
                except json.JSONDecodeError:
                    error = 'json decode error'
            else:
                error = 'http error'

            status = resp.status_code

        except requests.exceptions.ConnectionError as e:
            error = 'connection error: ' + str(e)
            status = 0
  
        return ApiResponse(status=status, request=payload, result=result, error=error)


    def retrieve_show_config(self, path=[]):
        return self._api_request(command="retrieve", op='showConfig', path=[], method="POST")

    def retrieve_return_values(self, path=[]):
        pass

    def reset(self, path=[]):
        pass

    def image_add(self):
        pass

    def image_delete(self):
        pass
    
    def show(self, path=[]):
        pass

    def generate(self, path=[]):
        pass

    def configure_sef(self, path=[]):
        pass

    def configure_delete(self, path=[]):
        pass

    def config_file_save(self, file=None):
        pass

    def config_file_load(self, file=None):
        pass

    