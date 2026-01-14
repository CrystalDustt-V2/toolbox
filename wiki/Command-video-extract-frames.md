# toolbox video extract-frames

Extract frames from video at intervals. Supports local or URL.

Source: [src/toolbox/plugins/video/__init__.py:L288](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/video/__init__.py#L288)

## Synopsis

```bash
toolbox video extract-frames INPUT_FILE [-i FLOAT] [-o PATH] [-f [jpg|png]] [--dry-run]
```

## Examples

```bash
toolbox video extract-frames <input_file>
toolbox video extract-frames -i <interval> -o <output_dir> <input_file>
```

## Help

```text
Usage: toolbox video extract-frames 
           [OPTIONS] INPUT_FILE

  Extract frames from video at intervals. Supports
  local or URL.

Options:
  -i, --interval FLOAT    Interval in seconds
                          between frames
  -o, --output-dir PATH   Output directory
  -f, --format [jpg|png]
  --dry-run               Show what would happen
  --help                  Show this message and
                          exit.
```

Parent: [toolbox video](Command-video)
Back: [Command Index](Command-Index)
