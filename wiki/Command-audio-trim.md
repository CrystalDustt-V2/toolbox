# toolbox audio trim

Trim an audio file. Supports local or URL.

Source: [src/toolbox/plugins/audio/__init__.py:L82](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/audio/__init__.py#L82)

## Synopsis

```bash
toolbox audio trim INPUT_FILE [--start TEXT] [--end TEXT] [-o PATH] [--dry-run]
```

## Examples

```bash
toolbox audio trim <input_file>
toolbox audio trim --start <start> --end <end> <input_file>
```

## Help

```text
Usage: toolbox audio trim [OPTIONS] INPUT_FILE

  Trim an audio file. Supports local or URL.

Options:
  --start TEXT       Start time (HH:MM:SS or
                     seconds)
  --end TEXT         End time (HH:MM:SS or seconds)
  -o, --output PATH
  --dry-run          Show what would happen
  --help             Show this message and exit.
```

Parent: [toolbox audio](Command-audio)
Back: [Command Index](Command-Index)
