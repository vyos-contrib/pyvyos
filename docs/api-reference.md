# API Reference

Complete reference for all PyVyOS classes and methods.

## VyDevice Class

Main class for interacting with VyOS devices.

### Constructor

```python
VyDevice(hostname: str, apikey: str, protocol: "http"|"https" = "https",
         port: int = 443, verify: bool = True, timeout: int = 10)
```

**Parameters:** `hostname`, `apikey`, `protocol`, `port` (1-65535), `verify`, `timeout`

### Configuration Methods

- `configure_set(path)`: Set configuration values
- `configure_delete(path)`: Delete configuration values
- `configure_multiple_op(op_path)`: Execute multiple operations atomically

```python
device.configure_set(path=["interfaces", "ethernet", "eth0", "address", "192.168.1.1/24"])
device.configure_delete(path=["interfaces", "dummy", "dum1"])
device.configure_multiple_op(op_path=[
    {"op": "set", "path": [...]},
    {"op": "delete", "path": [...]}
])
```

### Retrieval Methods

- `retrieve_show_config(path)`: Get configuration in show format
- `retrieve_return_values(path)`: Get specific configuration values

```python
device.retrieve_show_config(path=["system"])
device.retrieve_return_values(path=["interfaces", "dummy", "dum1", "address"])
```

### Operational Methods

- `show(path)`: Execute show commands
- `generate(path)`: Generate configuration elements
- `reset(path)`: Reset configuration elements

```python
device.show(path=["system", "image"])
device.generate(path=["ssh", "client-key", "/tmp/key"])
device.reset(path=["conntrack-sync", "internal-cache"])
```

### File Operations

- `config_file_save(file)`: Save configuration to file
- `config_file_load(file)`: Load configuration from file

```python
device.config_file_save(file="/config/backup.config")
device.config_file_load(file="/config/backup.config")
```

**Note:** The `path` parameter is automatically included as `[]` for config-file operations, as required by the VyOS API.

### System Operations

- `reboot(path=["now"])`: Reboot the device
- `poweroff(path=["now"])`: Power off the device

### Image Management

- `image_add(url, file, path)`: Add VyOS system image
- `image_delete(name, url, file, path)`: Delete a system image

## ApiResponse Class

Response object: `status` (int), `request` (dict, API key removed), `result` (dict), `error` (str|bool)

```python
response = device.show(path=["system"])
if response.error:
    print(f"Error {response.status}: {response.error}")
else:
    print(response.result)
```

