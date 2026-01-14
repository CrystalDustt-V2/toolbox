# toolbox audio merge

Merge multiple audio files into one. Supports local or URL.

Source: [src/toolbox/plugins/audio/__init__.py:L110](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/audio/__init__.py#L110)

## Synopsis

```bash
toolbox audio merge INPUT_FILES... [-o PATH] [--dry-run]
```

## Examples

```bash
toolbox audio merge <input_files>...
toolbox audio merge -o <output> --dry-run <input_files>...
```

## Help

```text
Usage: toolbox audio merge [OPTIONS] INPUT_FILES...

  Merge multiple audio files into one. Supports
  local or URL.

Options:
  -o, --output PATH
  --dry-run          Show what would happen
  --help             Show this message and exit.
```

Parent: [toolbox audio](Command-audio)
Back: [Command Index](Command-Index)
