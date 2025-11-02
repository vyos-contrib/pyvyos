# Troubleshooting

Common issues and solutions when using PyVyOS.

## Connection Issues

**Cannot Connect:** Verify hostname/IP, network connectivity, API enabled, firewall rules, port number.

**SSL Errors:** Use `verify=False` for dev (self-signed certs), install CA certs for production.

## Authentication Problems

**Invalid API Key:** Verify key is correct, check expiration, ensure permissions, regenerate if needed.

## Configuration Errors

**Invalid Path:** Verify path syntax matches VyOS tree, check path exists, use `retrieve_show_config` to inspect.

**Not Applied:** Call `config_file_save()` after changes, check commit requirements, verify permissions.

## Response Issues

**Empty Results:** Check if path has data, verify syntax, try broader path.

**Error Format:** Always check `response.error` first, inspect `response.status`, log full response.

## Performance Issues

**Timeouts:** Increase timeout parameter, check latency, verify device load, break into smaller operations.

**Slow Operations:** Use `configure_multiple_op` for bulk, avoid short polling, consider async for multiple devices.

## Environment Setup

**Variables Not Loading:** Verify `.env` exists, check `load_dotenv()` call, match variable names, use defaults.

## Debugging Tips

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Inspect full response
response = device.show(path=["system"])
print(f"Status: {response.status}, Error: {response.error}")
print(f"Result: {response.result}, Request: {response.request}")

# Test connection
response = device.show(path=["system", "host-name"])
if response.error:
    print(f"Connection issue: {response.error}")
```

## Getting Help

- Check [API Reference](api-reference.md) for method details
- Review [Examples](examples.md) for usage patterns
- Open issue on [GitHub](https://github.com/vyos-contrib/pyvyos/issues)

