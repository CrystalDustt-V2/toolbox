# toolbox doc inspect

Get basic information about a document. Supports local or URL.

## Synopsis

```bash
toolbox doc inspect [INPUT_FILE] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox doc inspect <input_file>
toolbox doc inspect --glob <glob_pattern> --parallel <input_file>
```

## Help

```text
Usage: toolbox doc inspect [OPTIONS] [INPUT_FILE]

  Get basic information about a document. Supports
  local or URL.

Options:
  --glob TEXT        Glob pattern to process
                     multiple files (e.g. '*.jpg')
  --parallel         Enable parallel processing for
                     batch operations
  --workers INTEGER  Number of worker threads
                     (default: CPU count)
  --help             Show this message and exit.
```

Parent: [toolbox doc](Command-doc)
Back: [Command Index](Command-Index)
