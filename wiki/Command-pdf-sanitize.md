# toolbox pdf sanitize

Remove metadata and hidden information from a PDF.

Source: [src/toolbox/plugins/pdf/__init__.py:L231](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/pdf/__init__.py#L231)

## Synopsis

```bash
toolbox pdf sanitize INPUT_FILE [-o TEXT] [--dry-run]
```

## Examples

```bash
toolbox pdf sanitize <input_file>
toolbox pdf sanitize -o <output> --dry-run <input_file>
```

## Help

```text
Usage: toolbox pdf sanitize [OPTIONS] INPUT_FILE

  Remove metadata and hidden information from a PDF.

Options:
  -o, --output TEXT  Output sanitized PDF path
  --dry-run          Show what would happen
  --help             Show this message and exit.
```

Parent: [toolbox pdf](Command-pdf)
Back: [Command Index](Command-Index)
