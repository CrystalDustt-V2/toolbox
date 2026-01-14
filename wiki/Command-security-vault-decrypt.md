# toolbox security vault-decrypt

Decrypt a .vault file.

Source: [src/toolbox/plugins/security/__init__.py:L193](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/security/__init__.py#L193)

## Synopsis

```bash
toolbox security vault-decrypt INPUT_FILE [--password TEXT] [-o PATH]
```

## Examples

```bash
toolbox security vault-decrypt <input_file>
toolbox security vault-decrypt --password <password> -o <output> <input_file>
```

## Help

```text
Usage: toolbox security vault-decrypt 
           [OPTIONS] INPUT_FILE

  Decrypt a .vault file.

Options:
  --password TEXT
  -o, --output PATH  Output decrypted file
  --help             Show this message and exit.
```

Parent: [toolbox security](Command-security)
Back: [Command Index](Command-Index)
