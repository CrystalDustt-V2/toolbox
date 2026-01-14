# toolbox file encrypt

Encrypt a file using AES-256-GCM.

Source: [src/toolbox/plugins/file/__init__.py:L181](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/file/__init__.py#L181)

## Synopsis

```bash
toolbox file encrypt INPUT_FILE [-o TEXT] [-p TEXT] [--dry-run]
```

## Examples

```bash
toolbox file encrypt <input_file>
toolbox file encrypt -o <output> -p <password> <input_file>
```

## Help

```text
Usage: toolbox file encrypt [OPTIONS] INPUT_FILE

  Encrypt a file using AES-256-GCM.

Options:
  -o, --output TEXT    Output encrypted file path
  -p, --password TEXT
  --dry-run            Show what would happen
  --help               Show this message and exit.
```

Parent: [toolbox file](Command-file)
Back: [Command Index](Command-Index)
