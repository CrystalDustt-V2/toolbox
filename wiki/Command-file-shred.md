# toolbox file shred

Securely erase a file by overwriting it multiple times (DoD 5220.22-M style).

Source: [src/toolbox/plugins/file/__init__.py:L264](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/file/__init__.py#L264)

## Synopsis

```bash
toolbox file shred INPUT_FILE [-p INTEGER] [--dry-run]
```

## Examples

```bash
toolbox file shred <input_file>
toolbox file shred -p <passes> --dry-run <input_file>
```

## Help

```text
Usage: toolbox file shred [OPTIONS] INPUT_FILE

  Securely erase a file by overwriting it multiple
  times (DoD 5220.22-M style).

Options:
  -p, --passes INTEGER  Number of overwrite passes
  --dry-run             Show what would happen
  --help                Show this message and exit.
```

Parent: [toolbox file](Command-file)
Back: [Command Index](Command-Index)
