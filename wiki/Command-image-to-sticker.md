# toolbox image to-sticker

Convert an image or GIF to a sticker. Supports local or URL.

Source: [src/toolbox/plugins/image/__init__.py:L254](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/image/__init__.py#L254)

## Synopsis

```bash
toolbox image to-sticker INPUT_FILE [-o PATH] [--pack TEXT] [--author TEXT] [--dry-run]
```

## Examples

```bash
toolbox image to-sticker <input_file>
toolbox image to-sticker -o <output> --pack <pack> <input_file>
```

## Help

```text
Usage: toolbox image to-sticker [OPTIONS] INPUT_FILE

  Convert an image or GIF to a sticker. Supports
  local or URL.

Options:
  -o, --output PATH  Output filename (must be .webp)
  --pack TEXT        Sticker pack name
  --author TEXT      Sticker author
  --dry-run          Show what would happen
  --help             Show this message and exit.
```

Parent: [toolbox image](Command-image)
Back: [Command Index](Command-Index)
