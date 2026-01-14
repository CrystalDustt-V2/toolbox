# toolbox video watermark

Add text or image watermark to a video.

Source: [src/toolbox/plugins/video/__init__.py:L318](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/video/__init__.py#L318)

## Synopsis

```bash
toolbox video watermark INPUT_FILE [-t TEXT] [-i PATH] [-o TEXT] [--pos [top-left|top-right|bottom-left|bottom-right|center]] [--dry-run]
```

## Examples

```bash
toolbox video watermark <input_file>
toolbox video watermark -t <text> -i <image> <input_file>
```

## Help

```text
Usage: toolbox video watermark [OPTIONS] INPUT_FILE

  Add text or image watermark to a video.

Options:
  -t, --text TEXT                 Text watermark to
                                  add
  -i, --image PATH                Image watermark to
                                  add
  -o, --output TEXT               Output filename
  --pos [top-left|top-right|bottom-left|bottom-right|center]
                                  Watermark position
  --dry-run                       Show what would
                                  happen
  --help                          Show this message
                                  and exit.
```

Parent: [toolbox video](Command-video)
Back: [Command Index](Command-Index)
