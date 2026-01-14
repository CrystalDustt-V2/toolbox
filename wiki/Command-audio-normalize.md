# toolbox audio normalize

Normalize audio volume using loudnorm filter. Supports local or URL.

Source: [src/toolbox/plugins/audio/__init__.py:L139](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/audio/__init__.py#L139)

## Synopsis

```bash
toolbox audio normalize INPUT_FILE [-o PATH] [--dry-run]
```

## Examples

```bash
toolbox audio normalize <input_file>
toolbox audio normalize -o <output> --dry-run <input_file>
```

## Help

```text
Usage: toolbox audio normalize [OPTIONS] INPUT_FILE

  Normalize audio volume using loudnorm filter.
  Supports local or URL.

Options:
  -o, --output PATH  Output filename
  --dry-run          Show what would happen
  --help             Show this message and exit.
```

Parent: [toolbox audio](Command-audio)
Back: [Command Index](Command-Index)
