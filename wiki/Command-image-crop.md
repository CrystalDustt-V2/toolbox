# toolbox image crop

Crop an image (left, top, right, bottom). Supports local or URL.

Source: [src/toolbox/plugins/image/__init__.py:L142](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/image/__init__.py#L142)

## Synopsis

```bash
toolbox image crop INPUT_FILE [--left INTEGER] [--top INTEGER] [--right INTEGER] [--bottom INTEGER] [-o PATH] [--dry-run]
```

## Examples

```bash
toolbox image crop <input_file>
toolbox image crop --left <left> --top <top> <input_file>
```

## Help

```text
Usage: toolbox image crop [OPTIONS] INPUT_FILE

  Crop an image (left, top, right, bottom). Supports
  local or URL.

Options:
  --left INTEGER     [required]
  --top INTEGER      [required]
  --right INTEGER    [required]
  --bottom INTEGER   [required]
  -o, --output PATH  Output filename
  --dry-run          Show what would happen without
                     actual cropping
  --help             Show this message and exit.
```

Parent: [toolbox image](Command-image)
Back: [Command Index](Command-Index)
