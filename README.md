# pyvyos Documentation

pyvyos is a Python library for interacting with VyOS devices via their API. This documentation provides a guide on how to use pyvyos to manage your VyOS devices programmatically.

You can find the complete pyvyos documentation on [Read the Docs](https://pyvyos.readthedocs.io/en/latest/).

## Installation

You can install pyvyos using pip https://pypi.org/project/pyvyos/:

```bash
pip install pyvyos
```

## Getting Started

### Importing and Disabling Warnings for verify=False
Before using pyvyos, it's a good practice to disable urllib3 warnings and import the required modules, IF you use verify=False:

```
import urllib3
urllib3.disable_warnings()
```

### Using API Response Class
pyvyos uses a custom ApiResponse data class to handle API responses:

```
@dataclass
class ApiResponse:
    status: int
    request: dict
    result: dict
    error: str
```

### Initializing a VyDevice Object


#### Configuring Your Environment for VyDevice
1. Rename the file .env.example to .env.
1. Open the .env file in a text editor.
1. Replace the placeholder values with your VyOS device credentials:
  - **VYDEVICE_HOSTNAME**: Your device's hostname or IP address.
  - **VYDEVICE_APIKEY**: Your API key for authentication.
  - **VYDEVICE_PORT**: The port number for the API. Default 443
  - **VYDEVICE_PROTOCOL**: The protocol (e.g., http or https). Default https
  - **VYDEVICE_VERIFY_SSL**: Set to True or False for SSL verification. 


```
# Retrieve VyOS device connection details from environment variables and configure VyDevice
from dotenv import load_dotenv
load_dotenv()

hostname = os.getenv('VYDEVICE_HOSTNAME')
apikey = os.getenv('VYDEVICE_APIKEY')
port = os.getenv('VYDEVICE_PORT')
protocol = os.getenv('VYDEVICE_PROTOCOL')
verify_ssl = os.getenv('VYDEVICE_VERIFY_SSL')

# Convert the verify_ssl value to a boolean
verify = verify_ssl.lower() == "true" if verify_ssl else True 

device = VyDevice(hostname=hostname, apikey=apikey, port=port, protocol=protocol, verify=verify)
```

## Using pyvyos

### configure, then set
The configure_set method sets a VyOS configuration:

```
# Set a VyOS configuration
response = device.configure_set(path=["interfaces", "ethernet", "eth0", "address", "192.168.1.1/24"])

# Check for errors and print the result
if not response.error:
    print(response.result)
```
### configure, then show a single OBJECT value
```
# Retrieve VyOS return values for a specific interface
response = device.retrieve_return_values(path=["interfaces", "dummy", "dum1", "address"])
print(response.result)
```

### configure, then show OBJECT
The retrieve_show_config method retrieves the VyOS configuration:

```
# Retrieve the VyOS configuration
response = device.retrieve_show_config(path=[])

# Check for errors and print the result
if not response.error:
    print(response.result)
```

### configure, then delete OBJECT
```
# Delete a VyOS interface configuration
response = device.configure_delete(path=["interfaces", "dummy", "dum1"])
```

### configure, then save
```
# Save VyOS configuration without specifying a file (default location)
response = device.config_file_save()
```

### configure, then save FILE
```
# Save VyOS configuration to a specific file
response = device.config_file_save(file="/config/test300.config")
```

## show OBJECT
```
# Show VyOS system image information
response = device.show(path=["system", "image"])
print(response.result)
```

### generate OBJECT
```
# Generate an SSH key with a random string in the name
randstring = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
keyrand =  f'/tmp/key_{randstring}'
response = device.generate(path=["ssh", "client-key", keyrand])
```

### reset OBJECT
The reset method allows you to run a reset command:

```
# Execute the reset command
response = device.reset(path=["conntrack-sync", "internal-cache"])

# Check for errors and print the result
if not response.error:
    print(response.result)
```

### configure, then load FILE
```
# Load VyOS configuration from a specific file
response = device.config_file_load(file="/config/test300.config")
```
