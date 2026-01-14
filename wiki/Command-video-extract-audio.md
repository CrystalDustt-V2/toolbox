# toolbox video extract-audio

Extract audio from a video file. Supports local or URL.

Source: [src/toolbox/plugins/video/__init__.py:L176](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/video/__init__.py#L176)

## Synopsis

```bash
toolbox video extract-audio INPUT_FILE [-o PATH] [--dry-run]
```

## Examples

```bash
toolbox video extract-audio <input_file>
toolbox video extract-audio -o <output> --dry-run <input_file>
```

## Help

```text
Usage: toolbox video extract-audio 
           [OPTIONS] INPUT_FILE

  Extract audio from a video file. Supports local or
  URL.

Options:
  -o, --output PATH
  --dry-run          Show what would happen
  --help             Show this message and exit.
```

Parent: [toolbox video](Command-video)
Back: [Command Index](Command-Index)
