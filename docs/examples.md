# Examples

Common usage patterns and examples for PyVyOS.

## Basic Connection

```python
from pyvyos import VyDevice
device = VyDevice(hostname="192.168.1.1", apikey="your-api-key", verify=False)
```

## Viewing System Information

```python
response = device.show(path=["system", "image"])
if not response.error:
    print(response.result)
```

## Interface Configuration

Add, view, get, or remove interface configuration:

```python
# Add address
device.configure_set(path=["interfaces", "ethernet", "eth0", "address", "192.168.1.1/24"])

# View configuration
device.retrieve_show_config(path=["interfaces", "ethernet", "eth0"])

# Get address value
device.retrieve_return_values(path=["interfaces", "ethernet", "eth0", "address"])

# Remove interface
device.configure_delete(path=["interfaces", "dummy", "dum1"])
```

## Multiple Operations

Execute multiple configuration changes atomically:

```python
device.configure_multiple_op(op_path=[
    {"op": "set", "path": ["interfaces", "dummy", "dum1", "address", "192.168.1.1/24"]},
    {"op": "set", "path": ["interfaces", "dummy", "dum1", "description", "Test"]},
    {"op": "delete", "path": ["interfaces", "dummy", "old1"]}
])
```

## Configuration Backup

```python
device.config_file_save(file="/config/backup-2024.config")
device.config_file_load(file="/config/backup-2024.config")
```

## SSH Key Generation

```python
import random, string
randstring = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
device.generate(path=["ssh", "client-key", f'/tmp/key_{randstring}'])
```

## System Operations

```python
device.reboot(path=["now"])
device.poweroff(path=["now"])
```

## Error Handling

```python
response = device.configure_set(path=["invalid", "path"])
if response.error:
    print(f"Error {response.status}: {response.error}")
else:
    print("Success:", response.result)
```

## Working with Responses

```python
response = device.show(path=["system"])
print(f"Status: {response.status}")
if not response.error:
    data = response.result  # Process data...
print(f"Request: {response.request}")  # API key sanitized
```

