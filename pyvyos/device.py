import urllib3
import requests
import json
import pprint
from dataclasses import dataclass

@dataclass
class ApiResponse:
    """
    Represents an API response.

    Attributes:
        status (int): The HTTP status code of the response.
        request (dict): The request payload sent to the API.
        result (dict): The data result of the API response.
        error (str): Any error message in case of a failed response.
    """
    status: int
    request: dict
    result: dict
    error: str

class VyDevice:
    """
    Represents a device for interacting with the VyOS API.

    Args:
        hostname (str): The hostname or IP address of the VyOS device.
        apikey (str): The API key for authentication.
        protocol (str, optional): The protocol to use (default is 'https').
        port (int, optional): The port to use (default is 443).
        verify (bool, optional): Whether to verify SSL certificates (default is True).
        timeout (int, optional): The request timeout in seconds (default is 10).

    Attributes:
        hostname (str): The hostname or IP address of the VyOS device.
        apikey (str): The API key for authentication.
        protocol (str): The protocol used for communication.
        port (int): The port used for communication.
        verify (bool): Whether SSL certificate verification is enabled.
        timeout (int): The request timeout in seconds.

    Methods:
        _get_url(command): Get the full URL for a given API command.
        _get_payload(op, path=[], file=None, url=None, name=None): Generate the API request payload.
        _api_request(command, op, path=[], method='POST', file=None, url=None, name=None): Make an API request.
        retrieve_show_config(path=[]): Retrieve and show the device configuration.
        retrieve_return_values(path=[]): Retrieve and return specific configuration values.
        reset(path=[]): Reset a specific configuration element.
        image_add(url=None, file=None, path=[]): Add an image from a URL or file.
        image_delete(name, url=None, file=None, path=[]): Delete a specific image.
        show(path=[]): Show configuration information.
        generate(path=[]): Generate configuration based on specified path.
        configure_set(path=[]): Sets configuration based on the specified path. This method is versatile, accepting 
        either a single configuration path or a list of configuration paths. This flexibility 
        allows for setting both individual and multiple configurations in a single operation.
        configure_delete(path=[]): Delete configuration based on specified path.
        config_file_save(file=None): Save the configuration to a file.
        config_file_load(file=None): Load the configuration from a file.
        reboot(path=["now"]): Reboot the device.
        poweroff(path=["now"]): Power off the device.
    """

    def __init__(self, hostname, apikey, protocol='https', port=443, verify=True, timeout=10):
        """
        Initializes a VyDevice instance.

        Args:
            hostname (str): The hostname or IP address of the VyOS device.
            apikey (str): The API key for authentication.
            protocol (str, optional): The protocol to use (default is 'https').
            port (int, optional): The port to use (default is 443).
            verify (bool, optional): Whether to verify SSL certificates (default is True).
            timeout (int, optional): The request timeout in seconds (default is 10).
        """
        self.hostname = hostname
        self.apikey = apikey
        self.protocol = protocol
        self.port = port
        self.verify = verify
        self.timeout = timeout

    def _get_url(self, command):
        """
        Get the full URL for a specific API command.

        Args:
            command (str): The API command to construct the URL for.

        Returns:
            str: The full URL for the API command.
        """
        return f"{self.protocol}://{self.hostname}:{self.port}/{command}"

    def _get_payload(self, op, path=[], file=None, url=None, name=None):
        """
        Generate the payload for an API request.

        Args:
            op (str): The operation to perform in the API request.
            path (list, optional): The path elements for the API request. This can be a single list for a single
                                configuration path or a list of lists for multiple configuration paths.
            file (str, optional): The file to include in the request (default is None).
            url (str, optional): The URL to include in the request (default is None).
            name (str, optional): The name to include in the request (default is None).

        Returns:
            dict: The payload for the API request.
        """
        # Adding option to pass multiple operation (eg:delete and set) commands
        if op:
            # Adjusting the data structure based on whether path is single or multiple
            if path and isinstance(path, list) and isinstance(path[0], list):  # Handling multiple paths
                data = [{'op': op, 'path': p} for p in path]
            else:  # Handling a single path
                data = {'op': op, 'path': path}
        else:
            if path and isinstance(path[0], dict):
                data = path

        # Including the optional parameters if provided
        if file:
            if isinstance(data, list):  # If data is a list of dicts (multiple paths)
                for d in data:
                    d['file'] = file
            else:  # If data is a single dict (single path)
                data['file'] = file
                
        if url:
            if isinstance(data, list):
                for d in data:
                    d['url'] = url
            else:
                data['url'] = url
            
        if name:
            if isinstance(data, list):
                for d in data:
                    d['name'] = name
            else:
                data['name'] = name
                
        payload = {
            'data': json.dumps(data),
            'key': self.apikey
        }

        return payload


    def _api_request(self, command, op, path=[], method='POST', file=None, url=None, name=None):
        """
        Make an API request.

        Args:
            command (str): The API command to execute.
            op (str): The operation to perform in the API request.
            path (list, optional): The path elements for the API request (default is an empty list).
            method (str, optional): The HTTP method to use for the request (default is 'POST').
            file (str, optional): The file to include in the request (default is None).
            url (str, optional): The URL to include in the request (default is None).
            name (str, optional): The name to include in the request (default is None).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        url = self._get_url(command)
        payload = self._get_payload(op, path=path, file=file, url=url, name=name)
        
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
  
        # Removing apikey from payload for security reasons
        del(payload['key'])
        return ApiResponse(status=status, request=payload, result=result, error=error)

    def retrieve_show_config(self, path=[]):
        """
        Retrieve and show the device configuration.

        Args:
            path (list, optional): The path elements for the configuration retrieval (default is an empty list).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="retrieve", op='showConfig', path=path, method="POST")

    def retrieve_return_values(self, path=[]):
        """
        Retrieve and return specific configuration values.

        Args:
            path (list, optional): The path elements for the configuration retrieval (default is an empty list).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="retrieve", op='returnValues', path=path, method="POST")

    def reset(self, path=[]):
        """
        Reset a specific configuration element.

        Args:
            path (list, optional): The path elements for the configuration reset (default is an empty list).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="reset", op='reset', path=path, method="POST")

    def image_add(self, url=None, file=None, path=[]):
        """
        Add an image from a URL or file.

        Args:
            url (str, optional): The URL of the image to add (default is None).
            file (str, optional): The path to the local image file to add (default is None).
            path (list, optional): The path elements for the image addition (default is an empty list).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="image", op='add', url=url, method="POST")

    def image_delete(self, name, url=None, file=None, path=[]):
        """
        Delete a specific image.

        Args:
            name (str): The name of the image to delete.
            url (str, optional): The URL of the image to delete (default is None).
            file (str, optional): The path to the local image file to delete (default is None).
            path (list, optional): The path elements for the image deletion (default is an empty list).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="image", op='delete', name=name, method="POST")

    def show(self, path=[]):
        """
        Show configuration information.

        Args:
            path (list, optional): The path elements for the configuration display (default is an empty list).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="show", op='show', path=path, method="POST")

    def generate(self, path=[]):
        """
        Generate configuration based on the given path.

        Args:
            path (list, optional): The path elements for configuration generation (default is an empty list).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="generate", op='generate', path=path, method="POST")

    def configure_set(self, path=[]):
        """
        Set configuration based on the given path.

        Args:
            path (list, optional): The path elements for configuration setting (default is an empty list).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="configure", op='set', path=path, method="POST")


    def configure_delete(self, path=[]):
        """
        Delete configuration based on the given path.

        Args:
            path (list, optional): The path elements for configuration deletion (default is an empty list).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="configure", op='delete', path=path, method="POST")

    def configure_multiple_op(self, op_path=[]):
        """
        Set configuration based on the given path for multiple operation.

        Args:
            op_path (list): The path elements for configuration deletion  or/and setting alongwith operations specific to them.
            eg: [{'op': 'delete', 'path': [...]}, {'op': 'set', 'path': [...]}]

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="configure", op=None, path=op_path)

    def config_file_save(self, file=None):
        """
        Save the configuration to a file.

        Args:
            file (str, optional): The path to the file where the configuration will be saved (default is None).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="config-file", op='save', file=file, method="POST")

    def config_file_load(self, file=None):
        """
        Load the configuration from a file.

        Args:
            file (str, optional): The path to the file from which the configuration will be loaded (default is None).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="config-file", op='load', file=file, method="POST")

    def reboot(self, path=["now"]):
        """
        Reboot the device.

        Args:
            path (list, optional): The path elements for the reboot operation (default is ["now"]).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="reboot", op='reboot', path=path, method="POST")
    
    def poweroff(self, path=["now"]):
        """
        Power off the device.

        Args:
            path (list, optional): The path elements for the power off operation (default is ["now"]).

        Returns:
            ApiResponse: An ApiResponse object representing the API response.
        """
        return self._api_request(command="poweroff", op='poweroff', path=path, method="POST")
