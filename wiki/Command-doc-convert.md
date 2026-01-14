# toolbox doc convert

Convert document format using LibreOffice. Supports local or URL.

## Synopsis

```bash
toolbox doc convert [INPUT_FILE] [--to TEXT] [-o PATH] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox doc convert <input_file>
toolbox doc convert --to <to> -o <output_dir> <input_file>
```

## Help

```text
Usage: toolbox doc convert [OPTIONS] [INPUT_FILE]

  Convert document format using LibreOffice.
  Supports local or URL.

Options:
  --to TEXT              Target format (e.g., pdf,
                         docx, html, txt)
                         [required]
  -o, --output-dir PATH  Output directory
  --dry-run              Show what would happen
  --glob TEXT            Glob pattern to process
                         multiple files (e.g.
                         '*.jpg')
  --parallel             Enable parallel processing
                         for batch operations
  --workers INTEGER      Number of worker threads
                         (default: CPU count)
  --help                 Show this message and exit.
```

Parent: [toolbox doc](Command-doc)
Back: [Command Index](Command-Index)
