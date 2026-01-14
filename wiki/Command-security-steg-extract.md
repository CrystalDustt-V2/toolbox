# toolbox security steg-extract

Extract hidden data from an image.

Source: [src/toolbox/plugins/security/__init__.py:L341](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/security/__init__.py#L341)

## Synopsis

```bash
toolbox security steg-extract IMAGE_FILE [--password TEXT] [-o PATH]
```

## Examples

```bash
toolbox security steg-extract <image_file>
toolbox security steg-extract --password <password> -o <output> <image_file>
```

## Help

```text
Usage: toolbox security steg-extract 
           [OPTIONS] IMAGE_FILE

  Extract hidden data from an image.

Options:
  --password TEXT    Password if data was encrypted
  -o, --output PATH  Output file for extracted data
  --help             Show this message and exit.
```

Parent: [toolbox security](Command-security)
Back: [Command Index](Command-Index)
