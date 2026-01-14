# toolbox video trim

Trim a video file. Supports local or URL.

Source: [src/toolbox/plugins/video/__init__.py:L148](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/video/__init__.py#L148)

## Synopsis

```bash
toolbox video trim INPUT_FILE [--start TEXT] [--end TEXT] [-o PATH] [--dry-run]
```

## Examples

```bash
toolbox video trim <input_file>
toolbox video trim --start <start> --end <end> <input_file>
```

## Help

```text
Usage: toolbox video trim [OPTIONS] INPUT_FILE

  Trim a video file. Supports local or URL.

Options:
  --start TEXT       Start time (HH:MM:SS)
  --end TEXT         End time (HH:MM:SS)
  -o, --output PATH
  --dry-run          Show what would happen
  --help             Show this message and exit.
```

Parent: [toolbox video](Command-video)
Back: [Command Index](Command-Index)
