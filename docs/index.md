# PyVyOS Documentation

PyVyOS is a Python SDK for interacting with VyOS devices via their REST API. This library provides a simple and intuitive interface to manage VyOS network devices programmatically.

## Overview

PyVyOS enables developers to:
- Configure VyOS devices remotely
- Retrieve configuration and operational data
- Manage system operations (reboot, poweroff)
- Generate SSH keys and manage images
- Save and load configuration files

## Documentation Structure

- [Installation](installation.md) - How to install PyVyOS
- [Getting Started](getting-started.md) - Quick start guide
- [API Reference](api-reference.md) - Complete API documentation
- [Configuration](configuration.md) - Device setup and authentication
- [Examples](examples.md) - Common usage patterns
- [Concepts](concepts.md) - Key concepts and architecture
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

## Requirements

- Python 3.13 or higher
- VyOS device with REST API enabled
- API key for authentication

## Quick Example

```python
from pyvyos import VyDevice

device = VyDevice(
    hostname="192.168.1.1",
    apikey="your-api-key",
    port=443,
    protocol="https",
    verify=True
)

response = device.show(path=["system", "image"])
print(response.result)
```

## Resources

- [GitHub Repository](https://github.com/vyos-contrib/pyvyos)
- [PyPI Package](https://pypi.org/project/pyvyos/)
## License

MIT License - See LICENSE file for details

