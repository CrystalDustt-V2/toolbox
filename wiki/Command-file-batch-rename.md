# toolbox file batch-rename

Batch rename files in a directory.

Source: [src/toolbox/plugins/file/__init__.py:L115](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/file/__init__.py#L115)

## Synopsis

```bash
toolbox file batch-rename DIRECTORY [-p TEXT] [-s TEXT] [-f TEXT] [-r TEXT] [-e TEXT] [--dry-run]
```

## Examples

```bash
toolbox file batch-rename <directory>
toolbox file batch-rename -p <prefix> -s <suffix> <directory>
```

## Help

```text
Usage: toolbox file batch-rename 
           [OPTIONS] DIRECTORY

  Batch rename files in a directory.

Options:
  -p, --prefix TEXT   Prefix for new filenames
  -s, --suffix TEXT   Suffix for new filenames
  -f, --find TEXT     String to find
  -r, --replace TEXT  String to replace with
  -e, --ext TEXT      Filter by extension (e.g.,
                      .jpg)
  --dry-run           Show what would happen
  --help              Show this message and exit.
```

Parent: [toolbox file](Command-file)
Back: [Command Index](Command-Index)
