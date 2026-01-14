# toolbox image ocr

Perform OCR on an image. Supports local or URL.

Source: [src/toolbox/plugins/image/__init__.py:L204](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/image/__init__.py#L204)

## Synopsis

```bash
toolbox image ocr INPUT_FILE [-l TEXT] [-o PATH] [--preprocess [none|grayscale|threshold]] [--scale FLOAT] [--dry-run]
```

## Examples

```bash
toolbox image ocr <input_file>
toolbox image ocr -l <lang> -o <output> <input_file>
```

## Help

```text
Usage: toolbox image ocr [OPTIONS] INPUT_FILE

  Perform OCR on an image. Supports local or URL.

Options:
  -l, --lang TEXT                 OCR language
                                  (default: eng)
  -o, --output PATH               Output text file
  --preprocess [none|grayscale|threshold]
                                  Image
                                  preprocessing
  --scale FLOAT                   Scale factor for
                                  the image
  --dry-run                       Show what would
                                  happen
  --help                          Show this message
                                  and exit.
```

Parent: [toolbox image](Command-image)
Back: [Command Index](Command-Index)
