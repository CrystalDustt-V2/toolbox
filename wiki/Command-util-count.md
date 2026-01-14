# toolbox util count

Count words, characters, and lines.

## Synopsis

```bash
toolbox util count [TEXT] [-f TEXT] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox util count <text>
toolbox util count -f <input_file> --glob <glob_pattern> <text>
```

## Help

```text
Usage: toolbox util count [OPTIONS] [TEXT]

  Count words, characters, and lines.

Options:
  -f, --input-file TEXT  Input file (Local or URL)
  --glob TEXT            Glob pattern to process
                         multiple files (e.g.
                         '*.jpg')
  --parallel             Enable parallel processing
                         for batch operations
  --workers INTEGER      Number of worker threads
                         (default: CPU count)
  --help                 Show this message and exit.
```

Parent: [toolbox util](Command-util)
Back: [Command Index](Command-Index)
