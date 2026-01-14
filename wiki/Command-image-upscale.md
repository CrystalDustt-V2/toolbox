# toolbox image upscale

Upscale image using AI (ESRGAN). Supports local or URL.

Source: [src/toolbox/plugins/image/__init__.py:L29](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/image/__init__.py#L29)

## Synopsis

```bash
toolbox image upscale INPUT_FILE [-o PATH] [-s INTEGER]
```

## Examples

```bash
toolbox image upscale <input_file>
toolbox image upscale -o <output> -s <scale> <input_file>
```

## Help

```text
Usage: toolbox image upscale [OPTIONS] INPUT_FILE

  Upscale image using AI (ESRGAN). Supports local or
  URL.

Options:
  -o, --output PATH    Output upscaled filename
  -s, --scale INTEGER  Upscale factor (2 or 4)
  --help               Show this message and exit.
```

Parent: [toolbox image](Command-image)
Back: [Command Index](Command-Index)
