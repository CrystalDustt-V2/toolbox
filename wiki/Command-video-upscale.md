# toolbox video upscale

Upscale video using AI (ESRGAN). WARNING: Very slow and resource-intensive.

Source: [src/toolbox/plugins/video/__init__.py:L26](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/video/__init__.py#L26)

## Synopsis

```bash
toolbox video upscale INPUT_FILE [-s INTEGER] [-o PATH] [--fps INTEGER]
```

## Examples

```bash
toolbox video upscale <input_file>
toolbox video upscale -s <scale> -o <output> <input_file>
```

## Help

```text
Usage: toolbox video upscale [OPTIONS] INPUT_FILE

  Upscale video using AI (ESRGAN). WARNING: Very
  slow and resource-intensive.

Options:
  -s, --scale INTEGER  Upscale factor (2 or 4)
  -o, --output PATH    Output upscaled video
                       filename
  --fps INTEGER        Override FPS (defaults to
                       original)
  --help               Show this message and exit.
```

Parent: [toolbox video](Command-video)
Back: [Command Index](Command-Index)
