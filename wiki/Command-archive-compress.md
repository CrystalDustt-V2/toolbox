# toolbox archive compress

Compress a file or directory.

Source: [src/toolbox/plugins/archive/__init__.py:L26](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/archive/__init__.py#L26)

## Synopsis

```bash
toolbox archive compress SOURCE [-o TEXT] [-f [zip|tar|gztar|bztar|xztar]] [--dry-run]
```

## Examples

```bash
toolbox archive compress <source>
toolbox archive compress -o <output> -f <format> <source>
```

## Help

```text
Usage: toolbox archive compress [OPTIONS] SOURCE

  Compress a file or directory.

Options:
  -o, --output TEXT               Output filename
                                  (without
                                  extension)
  -f, --format [zip|tar|gztar|bztar|xztar]
                                  Archive format
  --dry-run                       Show what would
                                  happen
  --help                          Show this message
                                  and exit.
```

Parent: [toolbox archive](Command-archive)
Back: [Command Index](Command-Index)
