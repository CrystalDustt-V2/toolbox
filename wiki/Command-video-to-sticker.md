# toolbox video to-sticker

Convert a video to a sticker. Supports local or URL.

Source: [src/toolbox/plugins/video/__init__.py:L248](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/video/__init__.py#L248)

## Synopsis

```bash
toolbox video to-sticker INPUT_FILE [-o PATH] [--fps INTEGER] [--dry-run]
```

## Examples

```bash
toolbox video to-sticker <input_file>
toolbox video to-sticker -o <output> --fps <fps> <input_file>
```

## Help

```text
Usage: toolbox video to-sticker [OPTIONS] INPUT_FILE

  Convert a video to a sticker. Supports local or
  URL.

Options:
  -o, --output PATH  Output filename
  --fps INTEGER      Sticker FPS
  --dry-run          Show what would happen
  --help             Show this message and exit.
```

Parent: [toolbox video](Command-video)
Back: [Command Index](Command-Index)
