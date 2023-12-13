# PyVyOS Documentation

PyVyOS is a Python library for interacting with VyOS devices via their API. This documentation provides a guide on how to use PyVyOS to manage your VyOS devices programmatically.

## Installation

You can install PyVyOS using pip:

```
bash
pip install pyvyos
```

## Getting Started

### Importing and Disabling Warnings for verify=False
Before using PyVyOS, it's a good practice to disable urllib3 warnings and import the required modules, IF you use verify=False:

```
import urllib3
urllib3.disable_warnings()
```

### Using API Response Class
PyVyOS uses a custom ApiResponse data class to handle API responses:

```
@dataclass
class ApiResponse:
    status: int
    request: dict
    result: dict
    error: str
```

### Initializing a VyDevice Object
To interact with your VyOS device, you'll need to create an instance of the VyDevice class. You can set up your device using the following code, 
assuming you've stored your credentials as environment variables:

```
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve VyOS device connection details from environment variables
hostname = os.getenv('VYDEVICE_HOSTNAME')
apikey = os.getenv('VYDEVICE_APIKEY')
port = os.getenv('VYDEVICE_PORT')
protocol = os.getenv('VYDEVICE_PROTOCOL')
verify_ssl = os.getenv('VYDEVICE_VERIFY_SSL')

# Convert the verify_ssl value to a boolean
verify = verify_ssl.lower() == "true" if verify_ssl else True

# Create an instance of the VyOS device
device = VyDevice(hostname=hostname, apikey=apikey, port=port, protocol=protocol, verify=verify)
```

## Using PyVyOS
Once you have created a VyDevice object, you can use it to interact with your VyOS device using various methods provided by the library.


### Reset
The reset method allows you to run a reset command:

```
# Execute the reset command
response = device.reset(path=["conntrack-sync", "internal-cache"])

# Check for errors and print the result
if not response.error:
    print(response.result)
```

### Retrieve Show Configuration
The retrieve_show_config method retrieves the VyOS configuration:

```
# Retrieve the VyOS configuration
response = device.retrieve_show_config(path=[])

# Check for errors and print the result
if not response.error:
    print(response.result)
```

### Retrieve Return Values
```
# Retrieve VyOS return values for a specific interface
response = device.retrieve_return_values(path=["interfaces", "dummy", "dum1", "address"])
print(response.result)
```

### Configure Delete
```
# Delete a VyOS interface configuration
response = device.configure_delete(path=["interfaces", "dummy", "dum1"])
```

### Generate
```
# Generate an SSH key with a random string in the name
randstring = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
keyrand =  f'/tmp/key_{randstring}'
response = device.generate(path=["ssh", "client-key", keyrand])
```

### Show
```
# Show VyOS system image information
response = device.show(path=["system", "image"])
print(response.result)
```

### Reset
```
# Reset VyOS with specific parameters
response = device.reset(path=["conntrack-sync", "internal-cache"])
```

### Configure Set
The configure_set method sets a VyOS configuration:

```
# Set a VyOS configuration
response = device.configure_set(path=["interfaces ethernet eth0 address '192.168.1.1/24'"])

# Check for errors and print the result
if not response.error:
    print(response.result)
```

### Config File Save 
```
# Save VyOS configuration without specifying a file (default location)
response = device.config_file_save()
```

### Config File Save with custom filename
```
# Save VyOS configuration to a specific file
response = device.config_file_save(file="/config/test300.config")
```

### Config File Load
```
# Load VyOS configuration from a specific file
response = device.config_file_load(file="/config/test300.config")
```