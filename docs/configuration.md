# Configuration

Guide to configuring PyVyOS for connecting to VyOS devices.

## Environment Variables

The recommended way to configure PyVyOS is using environment variables with a `.env` file.

### Required Variables

- `VYDEVICE_HOSTNAME`: IP address or hostname of your VyOS device
- `VYDEVICE_APIKEY`: API key for authentication

### Optional Variables

- `VYDEVICE_PORT`: API port (default: 443)
- `VYDEVICE_PROTOCOL`: Protocol "http" or "https" (default: https)
- `VYDEVICE_VERIFY_SSL`: "True" or "False" (default: True)

## .env File Setup

Create a `.env` file in your project root:

```bash
VYDEVICE_HOSTNAME=192.168.1.1
VYDEVICE_APIKEY=your-secret-api-key
VYDEVICE_PORT=443
VYDEVICE_PROTOCOL=https
VYDEVICE_VERIFY_SSL=False
```

## Loading Configuration

```python
from dotenv import load_dotenv
import os
from pyvyos import VyDevice

load_dotenv()
device = VyDevice(
    hostname=os.getenv('VYDEVICE_HOSTNAME'),
    apikey=os.getenv('VYDEVICE_APIKEY'),
    port=int(os.getenv('VYDEVICE_PORT', 443)),
    protocol=os.getenv('VYDEVICE_PROTOCOL', 'https'),
    verify=os.getenv('VYDEVICE_VERIFY_SSL', 'True').lower() == 'true'
)
```

## Direct Configuration

Pass parameters directly:

```python
device = VyDevice(hostname="192.168.1.1", apikey="your-api-key",
                  port=443, protocol="https", verify=False, timeout=30)
```

## SSL & Timeout

SSL verification enabled by default. To disable (dev only):

```python
import urllib3
urllib3.disable_warnings()
device = VyDevice(..., verify=False, timeout=60)
```

## Generating API Key on VyOS

1. SSH into your VyOS device
2. Run: `configure`
3. Run: `set system api http interface <interface>`
4. Run: `set system api http port <port>`
5. Run: `set system api http api-key <key-name> key <key-value>`
6. Run: `commit` and `save`

## Security Best Practices

- Never commit `.env` files to version control
- Use strong API keys
- Enable SSL verification in production
- Restrict API access to specific interfaces/IPs on VyOS
- Rotate API keys regularly

