# toolbox security vault-encrypt

Encrypt a file into a secure vault (.vault).

Source: [src/toolbox/plugins/security/__init__.py:L174](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/security/__init__.py#L174)

## Synopsis

```bash
toolbox security vault-encrypt INPUT_FILE [--password TEXT] [-o PATH]
```

## Examples

```bash
toolbox security vault-encrypt <input_file>
toolbox security vault-encrypt --password <password> -o <output> <input_file>
```

## Help

```text
Usage: toolbox security vault-encrypt 
           [OPTIONS] INPUT_FILE

  Encrypt a file into a secure vault (.vault).

Options:
  --password TEXT
  -o, --output PATH  Output encrypted file
  --help             Show this message and exit.
```

Parent: [toolbox security](Command-security)
Back: [Command Index](Command-Index)
