# toolbox pdf ocr

Perform OCR on a PDF. Supports local or URL.

## Synopsis

```bash
toolbox pdf ocr [INPUT_FILE] [-l TEXT] [-o PATH] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox pdf ocr <input_file>
toolbox pdf ocr -l <lang> -o <output> <input_file>
```

## Help

```text
Usage: toolbox pdf ocr [OPTIONS] [INPUT_FILE]

  Perform OCR on a PDF. Supports local or URL.

Options:
  -l, --lang TEXT    OCR language (default: eng)
  -o, --output PATH  Output text file
  --dry-run          Show what would happen
  --glob TEXT        Glob pattern to process
                     multiple files (e.g. '*.jpg')
  --parallel         Enable parallel processing for
                     batch operations
  --workers INTEGER  Number of worker threads
                     (default: CPU count)
  --help             Show this message and exit.
```

Parent: [toolbox pdf](Command-pdf)
Back: [Command Index](Command-Index)
