# toolbox security quantum-encrypt

Encrypt a file using Quantum-Resistant Hybrid AES-256-GCM.

Source: [src/toolbox/plugins/security/__init__.py:L214](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/security/__init__.py#L214)

## Synopsis

```bash
toolbox security quantum-encrypt INPUT_FILE [--password TEXT] [-o PATH]
```

## Examples

```bash
toolbox security quantum-encrypt <input_file>
toolbox security quantum-encrypt --password <password> -o <output> <input_file>
```

## Help

```text
Usage: toolbox security quantum-encrypt 
           [OPTIONS] INPUT_FILE

  Encrypt a file using Quantum-Resistant Hybrid
  AES-256-GCM.

Options:
  --password TEXT
  -o, --output PATH  Output file
  --help             Show this message and exit.
```

Parent: [toolbox security](Command-security)
Back: [Command Index](Command-Index)
