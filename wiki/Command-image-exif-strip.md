# toolbox image exif-strip

Remove EXIF metadata from an image. Supports local or URL.

Source: [src/toolbox/plugins/image/__init__.py:L184](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/image/__init__.py#L184)

## Synopsis

```bash
toolbox image exif-strip INPUT_FILE [-o PATH] [--dry-run]
```

## Examples

```bash
toolbox image exif-strip <input_file>
toolbox image exif-strip -o <output> --dry-run <input_file>
```

## Help

```text
Usage: toolbox image exif-strip [OPTIONS] INPUT_FILE

  Remove EXIF metadata from an image. Supports local
  or URL.

Options:
  -o, --output PATH  Output filename
  --dry-run          Show what would happen
  --help             Show this message and exit.
```

Parent: [toolbox image](Command-image)
Back: [Command Index](Command-Index)
