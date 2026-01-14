# toolbox file decrypt

Decrypt a file using AES-256-GCM.

Source: [src/toolbox/plugins/file/__init__.py:L223](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/file/__init__.py#L223)

## Synopsis

```bash
toolbox file decrypt INPUT_FILE [-o TEXT] [-p TEXT] [--dry-run]
```

## Examples

```bash
toolbox file decrypt <input_file>
toolbox file decrypt -o <output> -p <password> <input_file>
```

## Help

```text
Usage: toolbox file decrypt [OPTIONS] INPUT_FILE

  Decrypt a file using AES-256-GCM.

Options:
  -o, --output TEXT    Output decrypted file path
  -p, --password TEXT
  --dry-run            Show what would happen
  --help               Show this message and exit.
```

Parent: [toolbox file](Command-file)
Back: [Command Index](Command-Index)
