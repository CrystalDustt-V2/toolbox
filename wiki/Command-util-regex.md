# toolbox util regex

Extract text using regex pattern. Supports local or URL.

## Synopsis

```bash
toolbox util regex PATTERN [INPUT_FILE] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox util regex <pattern> <input_file>
toolbox util regex --glob <glob_pattern> --parallel <pattern> <input_file>
```

## Help

```text
Usage: toolbox util regex [OPTIONS] PATTERN
                          [INPUT_FILE]

  Extract text using regex pattern. Supports local
  or URL.

Options:
  --glob TEXT        Glob pattern to process
                     multiple files (e.g. '*.jpg')
  --parallel         Enable parallel processing for
                     batch operations
  --workers INTEGER  Number of worker threads
                     (default: CPU count)
  --help             Show this message and exit.
```

Parent: [toolbox util](Command-util)
Back: [Command Index](Command-Index)
