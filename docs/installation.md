# Installation

## Prerequisites

PyVyOS requires Python 3.13 or higher. Make sure you have a compatible Python version installed.

## Using pip

The recommended way to install PyVyOS is using pip:

```bash
pip install pyvyos
```

## Using uv

If you use `uv` for package management:

```bash
uv add pyvyos
```

## From Source

To install from source:

```bash
git clone https://github.com/vyos-contrib/pyvyos.git
cd pyvyos
pip install .
```

## Verify Installation

After installation, verify it works:

```python
from pyvyos import VyDevice
print("PyVyOS installed successfully")
```

## Dependencies

PyVyOS automatically installs:
- `requests>=2.32.0` - HTTP library for API calls
- `python-dotenv>=1.0.1` - Environment variable management
- `urllib3>=2.5.0` - HTTP client utilities

## Development Installation

For development with testing support:

```bash
pip install pyvyos[dev]
```

This includes:
- `pytest>=6.2.5` - Testing framework
- `pytest-cov>=4.1` - Coverage reporting
- `pytest-env>=0.6.2` - Environment variable testing

## Next Steps

After installation, proceed to [Getting Started](getting-started.md) to configure your first device connection.

