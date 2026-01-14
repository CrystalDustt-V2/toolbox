# toolbox video remove-watermark

Remove a watermark from a specific area using the delogo filter.

Source: [src/toolbox/plugins/video/__init__.py:L378](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/video/__init__.py#L378)

## Synopsis

```bash
toolbox video remove-watermark INPUT_FILE [-x INTEGER] [-y INTEGER] [-w INTEGER] [-h INTEGER] [-o TEXT] [--dry-run]
```

## Examples

```bash
toolbox video remove-watermark <input_file>
toolbox video remove-watermark -x <x> -y <y> <input_file>
```

## Help

```text
Usage: toolbox video remove-watermark 
           [OPTIONS] INPUT_FILE

  Remove a watermark from a specific area using the
  delogo filter.

Options:
  -x INTEGER            X coordinate of the
                        watermark  [required]
  -y INTEGER            Y coordinate of the
                        watermark  [required]
  -w, --width INTEGER   Width of the watermark
                        [required]
  -h, --height INTEGER  Height of the watermark
                        [required]
  -o, --output TEXT     Output filename
  --dry-run             Show what would happen
  --help                Show this message and exit.
```

Parent: [toolbox video](Command-video)
Back: [Command Index](Command-Index)
