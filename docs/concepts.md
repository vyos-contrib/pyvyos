# Concepts

Key concepts and architecture of PyVyOS.

## Architecture Overview

PyVyOS is built on a REST client architecture:
- `RestClient`: Base class handling HTTP communication
- `VyDevice`: High-level interface for VyOS operations
- `ApiResponse`: Standardized response structure

## API Command Structure

VyOS API uses a hierarchical command structure:
- Commands: `configure`, `retrieve`, `show`, `generate`, `reset`
- Operations: `set`, `delete`, `showConfig`, `returnValues`
- Paths: Array representing configuration hierarchy

## Path Format

Paths are always arrays representing the configuration tree:

```python
# Single path
["interfaces", "ethernet", "eth0", "address", "192.168.1.1/24"]

# Multiple paths (for configure_set)
[
    ["interfaces", "ethernet", "eth0", "address", "192.168.1.1/24"],
    ["interfaces", "ethernet", "eth0", "description", "Management"]
]
```

## Response Handling

All methods return `ApiResponse`:
- Consistent error checking
- Sanitized request payloads (API keys removed)
- Structured result data

## Operation Types

### Configuration Operations
- `set`: Add or modify configuration
- `delete`: Remove configuration
- `showConfig`: Get full configuration
- `returnValues`: Get specific values

### Operational Commands
- `show`: Execute show commands
- `generate`: Generate configurations/keys
- `reset`: Reset state/cache

## Multi-Operation Requests

`configure_multiple_op` allows atomic operations:
- Multiple set/delete operations in one API call
- Transaction-like behavior
- Better performance than individual calls

## Error Handling Strategy

PyVyOS uses defensive error handling:
- Network errors captured as exceptions
- API errors returned in response.error
- HTTP status codes in response.status

## Security Considerations

- API keys never appear in response.request
- SSL verification configurable per connection
- Timeout protection prevents hanging connections

## Connection Lifecycle

1. Initialize VyDevice with connection parameters
2. Parameters validated on initialization
3. Each method creates new HTTP request
4. Responses parsed and returned as ApiResponse

## Best Practices

- Use environment variables for credentials
- Enable SSL verification in production
- Handle errors explicitly
- Use configure_multiple_op for bulk changes
- Set appropriate timeouts for operations

