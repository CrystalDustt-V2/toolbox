# toolbox pdf merge

Merge multiple PDF files into one. Supports local or URL.

Source: [src/toolbox/plugins/pdf/__init__.py:L29](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/pdf/__init__.py#L29)

## Synopsis

```bash
toolbox pdf merge INPUTS... [-o PATH] [--dry-run]
```

## Examples

```bash
toolbox pdf merge <inputs>...
toolbox pdf merge -o <output> --dry-run <inputs>...
```

## Help

```text
Usage: toolbox pdf merge [OPTIONS] INPUTS...

  Merge multiple PDF files into one. Supports local
  or URL.

Options:
  -o, --output PATH  Output filename
  --dry-run          Show what would happen
  --help             Show this message and exit.
```

Parent: [toolbox pdf](Command-pdf)
Back: [Command Index](Command-Index)
