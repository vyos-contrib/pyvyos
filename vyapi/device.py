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
    def __init__(self, hostname, apikey, protocol='https', port=443, verify=True, timeout=10):
        self.hostname = hostname
        self.apikey = apikey
        self.protocol = protocol
        self.port = port
        self.verify = verify
        self.timeout = timeout


    def _get_url(self, command):
        return f"{self.protocol}://{self.hostname}:{self.port}/{command}"

    def _get_payload(self, op, path, file=None):
        if file is not None:
            return {
                'data': json.dumps({
                    'op': op, 
                    'file': file,
                }),
                'key': self.apikey
            }
        else:           
            return {
                'data': json.dumps({'op': op, 'path': path}),
                'key': self.apikey
            }

    def _api_request(self, command, op, path=[], method='POST', file=None):
        url = self._get_url(command)
        payload = self._get_payload(op, path, file)
        pprint.pprint(payload)
        
        headers = {}
        error = False      
        result = {}

        try:
            resp = requests.post(url, verify=self.verify, data=payload, timeout=self.timeout, headers=headers)
            pprint.pprint(resp.text)
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
        return self._api_request(command="retrieve", op='showConfig', path=path, method="POST")

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

    def configure_set(self, path=[]):
        return self._api_request(command="configure", op='set', path=path, method="POST")

    def configure_delete(self, path=[]):
        return self._api_request(command="configure", op='delete', path=path, method="POST")

    def config_file_save(self, file=None):
        return self._api_request(command="config-file", op='save', file=file, method="POST")

    def config_file_load(self, file=None):
        return self._api_request(command="config-file", op='load', file=file, method="POST")


    