# Getting Started

This guide will help you set up PyVyOS and make your first API call to a VyOS device.

## Prerequisites

- VyOS device with REST API enabled
- API key generated on your VyOS device
- Network access to your VyOS device

## Step 1: Install PyVyOS

See [Installation](installation.md) for detailed instructions.

## Step 2: Configure Environment Variables

Create a `.env` file in your project directory:

```bash
VYDEVICE_HOSTNAME=192.168.1.1
VYDEVICE_APIKEY=your-api-key-here
VYDEVICE_PORT=443
VYDEVICE_PROTOCOL=https
VYDEVICE_VERIFY_SSL=true
```

## Step 3: Create Your First Script

```python
import os
from dotenv import load_dotenv
from pyvyos import VyDevice

load_dotenv()

device = VyDevice(
    hostname=os.getenv('VYDEVICE_HOSTNAME'),
    apikey=os.getenv('VYDEVICE_APIKEY'),
    port=os.getenv('VYDEVICE_PORT'),
    protocol=os.getenv('VYDEVICE_PROTOCOL'),
    verify=os.getenv('VYDEVICE_VERIFY_SSL', 'True').lower() == 'true'
)

response = device.show(path=["system", "image"])
if not response.error:
    print(response.result)
else:
    print(f"Error: {response.error}")
```

## Step 4: Disable SSL Warnings (Optional)

If using `verify=False`, disable urllib3 warnings:

```python
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

## Understanding API Responses

All methods return an `ApiResponse` object with:
- `status`: HTTP status code
- `request`: Request payload (API key sanitized)
- `result`: Response data dictionary
- `error`: Error message (False if successful)

## Common Operations

See [Examples](examples.md) for more detailed usage patterns.

## Next Steps

- Read [API Reference](api-reference.md) for complete method documentation
- Explore [Configuration](configuration.md) for advanced setup
- Check [Concepts](concepts.md) to understand PyVyOS architecture

