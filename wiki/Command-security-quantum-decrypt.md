# toolbox security quantum-decrypt

Decrypt a .qvault file using hardware-bound keys.

Source: [src/toolbox/plugins/security/__init__.py:L248](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/security/__init__.py#L248)

## Synopsis

```bash
toolbox security quantum-decrypt INPUT_FILE [--password TEXT] [-o PATH]
```

## Examples

```bash
toolbox security quantum-decrypt <input_file>
toolbox security quantum-decrypt --password <password> -o <output> <input_file>
```

## Help

```text
Usage: toolbox security quantum-decrypt 
           [OPTIONS] INPUT_FILE

  Decrypt a .qvault file using hardware-bound keys.

Options:
  --password TEXT
  -o, --output PATH  Output file
  --help             Show this message and exit.
```

Parent: [toolbox security](Command-security)
Back: [Command Index](Command-Index)
