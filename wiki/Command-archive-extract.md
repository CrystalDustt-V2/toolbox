# toolbox archive extract

Extract an archive file. Supports local or URL.

Source: [src/toolbox/plugins/archive/__init__.py:L48](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/archive/__init__.py#L48)

## Synopsis

```bash
toolbox archive extract ARCHIVE [-o PATH] [--dry-run]
```

## Examples

```bash
toolbox archive extract <archive>
toolbox archive extract -o <output_dir> --dry-run <archive>
```

## Help

```text
Usage: toolbox archive extract [OPTIONS] ARCHIVE

  Extract an archive file. Supports local or URL.

Options:
  -o, --output-dir PATH  Directory to extract into
  --dry-run              Show what would happen
  --help                 Show this message and exit.
```

Parent: [toolbox archive](Command-archive)
Back: [Command Index](Command-Index)
