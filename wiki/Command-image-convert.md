# toolbox image convert

Convert image format (e.g., photo.jpg photo.png). Supports local or URL.

## Synopsis

```bash
toolbox image convert [INPUT_FILE] [OUTPUT_FILE] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox image convert <input_file> <output_file>
toolbox image convert --glob <glob_pattern> --parallel <input_file> <output_file>
```

## Help

```text
Usage: toolbox image convert [OPTIONS] [INPUT_FILE]
                             [OUTPUT_FILE]

  Convert image format (e.g., photo.jpg photo.png).
  Supports local or URL.

Options:
  --glob TEXT        Glob pattern to process
                     multiple files (e.g. '*.jpg')
  --parallel         Enable parallel processing for
                     batch operations
  --workers INTEGER  Number of worker threads
                     (default: CPU count)
  --help             Show this message and exit.
```

Parent: [toolbox image](Command-image)
Back: [Command Index](Command-Index)
