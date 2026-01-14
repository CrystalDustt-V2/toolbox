# toolbox security vault-announce

Announce a vault to the local network for discovery.

Source: [src/toolbox/plugins/security/__init__.py:L408](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/security/__init__.py#L408)

## Synopsis

```bash
toolbox security vault-announce VAULT_PATH [--name TEXT]
```

## Examples

```bash
toolbox security vault-announce <vault_path>
toolbox security vault-announce --name <name> <vault_path>
```

## Help

```text
Usage: toolbox security vault-announce 
           [OPTIONS] VAULT_PATH

  Announce a vault to the local network for
  discovery.

Options:
  --name TEXT  Display name for this vault
  --help       Show this message and exit.
```

Parent: [toolbox security](Command-security)
Back: [Command Index](Command-Index)
