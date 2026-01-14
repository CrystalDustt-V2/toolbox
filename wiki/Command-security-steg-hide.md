# toolbox security steg-hide

Hide a file inside an image using LSB steganography (optionally encrypted).

Source: [src/toolbox/plugins/security/__init__.py:L281](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/security/__init__.py#L281)

## Synopsis

```bash
toolbox security steg-hide IMAGE_FILE SECRET_FILE [--password TEXT] [-o PATH]
```

## Examples

```bash
toolbox security steg-hide <image_file> <secret_file>
toolbox security steg-hide --password <password> -o <output> <image_file> <secret_file>
```

## Help

```text
Usage: toolbox security steg-hide 
           [OPTIONS] IMAGE_FILE SECRET_FILE

  Hide a file inside an image using LSB
  steganography (optionally encrypted).

Options:
  --password TEXT    Optional password to encrypt
                     hidden data
  -o, --output PATH  Output image with hidden data
  --help             Show this message and exit.
```

Parent: [toolbox security](Command-security)
Back: [Command Index](Command-Index)
