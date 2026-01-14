# toolbox file hash

Calculate file checksum/hash. Supports local or URL.

Source: [src/toolbox/plugins/file/__init__.py:L77](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/file/__init__.py#L77)

## Synopsis

```bash
toolbox file hash INPUT_SOURCE [-a [md5|sha1|sha256|sha512]] [--dry-run]
```

## Examples

```bash
toolbox file hash <input_source>
toolbox file hash -a <algorithm> --dry-run <input_source>
```

## Help

```text
Usage: toolbox file hash [OPTIONS] INPUT_SOURCE

  Calculate file checksum/hash. Supports local or
  URL.

Options:
  -a, --algorithm [md5|sha1|sha256|sha512]
  --dry-run                       Show what would
                                  happen
  --help                          Show this message
                                  and exit.
```

Parent: [toolbox file](Command-file)
Back: [Command Index](Command-Index)
