import json
from dataclasses import dataclass
from typing import List, Tuple

from requests import Request, Response
from requests.exceptions import HTTPError, ConnectionError
import requests


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


class RestClient:

    def __init__(
        self,
        hostname: str,
        apikey: str,
        protocol: str,
        port: int,
        verify: bool,
        timeout: int,
    ):
        """
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

    def _get_payload(self, op, path: List = None, file=None, url=None, name=None):
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
        if path is None:
            path = []

        if op:
            # Adjusting the data structure based on whether path is single or multiple
            if (
                path and isinstance(path, list) and isinstance(path[0], list)
            ):  # Handling multiple paths
                data = [{"op": op, "path": p} for p in path]
            else:  # Handling a single path
                data = {"op": op, "path": path}
        else:
            if path and isinstance(path[0], dict):
                data = path

        # Including the optional parameters if provided
        if file:
            if isinstance(data, list):  # If data is a list of dicts (multiple paths)
                for d in data:
                    d["file"] = file
            else:  # If data is a single dict (single path)
                data["file"] = file

        if url:
            if isinstance(data, list):
                for d in data:
                    d["url"] = url
            else:
                data["url"] = url

        if name:
            if isinstance(data, list):
                for d in data:
                    d["name"] = name
            else:
                data["name"] = name

        payload = {"data": json.dumps(data), "key": self.apikey}

        return payload

    def _api_request(
        self, command, op, path=[], method="POST", file=None, url=None, name=None
    ):
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

        resp = requests.post(
            url,
            verify=self.verify,
            data=payload,
            timeout=self.timeout,
            headers=headers,
        )
        status, result, error = self._validate_response(resp)

        # Removing apikey from payload for security reasons
        del payload["key"]
        return ApiResponse(status=status, request=payload, result=result, error=error)

    @classmethod
    def _validate_response(cls, resp: Response) -> Tuple:
        status = None
        result = {}

        try:
            resp.raise_for_status()
            resp_decoded = resp.json()
            if resp_decoded["success"]:
                result = resp_decoded["data"]
                error = False
            else:
                error = resp_decoded["error"]

            status = resp.status_code

        except json.JSONDecodeError as exc:
            error = "JSONDecodeError: " + str(exc)

        except (ConnectionError, HTTPError) as exc:
            error = "API Error: " + str(exc.response.text)
            status = exc.response.status_code

        return status, result, error
