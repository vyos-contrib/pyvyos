# VyOS API Command Reference

The JSON definitions for each VyOS REST API command supported by PyVyOS are located in `docs/development/vyos_api/`.

## Location

All JSON specification files are stored in: **`docs/development/vyos_api/`**

These JSONs are reference documentation and are:
- Used for API documentation generation
- Available for validation and testing
- Not packaged with the library (reference only)

## Files

- `schema.json` - JSON Schema definition for all API commands
- Individual command files:
  - `configure-set.json` - Set configuration values
  - `configure-delete.json` - Delete configuration values
  - `configure-multiple-op.json` - Execute multiple operations atomically
  - `retrieve-show-config.json` - Retrieve configuration in show format
  - `retrieve-return-values.json` - Retrieve specific configuration values
  - `show.json` - Execute show commands
  - `generate.json` - Generate configuration elements (SSH keys, etc.)
  - `reset.json` - Reset configuration elements
  - `config-file-save.json` - Save configuration to file
  - `config-file-load.json` - Load configuration from file
  - `reboot.json` - Reboot the device
  - `poweroff.json` - Power off the device
  - `image-add.json` - Add VyOS system image
  - `image-delete.json` - Delete VyOS system image

## Structure

Each JSON file follows this structure:

```json
{
  "command": "command-name",
  "operation": "operation-name",
  "description": "Description of what the command does",
  "endpoint": "/endpoint-path",
  "method": "HTTP_METHOD",
  "request": {
    "payload": { ... },
    "example": { ... }
  },
  "response": {
    "success": { ... },
    "error": { ... }
  },
  "parameters": { ... },
  "python_usage": "device.method_name(...)"
}
```

## Usage

These JSON files can be used for:
- API documentation generation
- Request validation
- Response schema validation
- Client library code generation
- Testing and mocking

## JSON Schema

The `schema.json` file defines the complete structure for all API commands and can be used with JSON Schema validators.

## Path Parameter Handling

**Important:** The `path` parameter handling varies by command:

- **config-file commands** (`save`, `load`): The VyOS API requires `path` to be present in the payload, even if empty (`[]`). PyVyOS handles this automatically.
- **Other commands**: When `path` is empty or not provided, it may be omitted from the payload for cleaner requests.

See individual JSON files in `docs/development/vyos_api/` for specific parameter requirements.

