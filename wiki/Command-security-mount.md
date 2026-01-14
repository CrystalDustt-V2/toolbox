# toolbox security mount

Mount an encrypted vault as a temporary virtual drive.

Source: [src/toolbox/plugins/security/__init__.py:L124](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/security/__init__.py#L124)

## Synopsis

```bash
toolbox security mount VAULT_FILE [--password TEXT] [--drive TEXT]
```

## Examples

```bash
toolbox security mount <vault_file>
toolbox security mount --password <password> --drive <drive> <vault_file>
```

## Help

```text
Usage: toolbox security mount [OPTIONS] VAULT_FILE

  Mount an encrypted vault as a temporary virtual
  drive.

Options:
  --password TEXT
  --drive TEXT     Drive letter (Windows only, e.g.,
                   T:)
  --help           Show this message and exit.
```

Parent: [toolbox security](Command-security)
Back: [Command Index](Command-Index)
