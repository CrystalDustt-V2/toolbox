# toolbox video to-gif

Convert video to GIF. Supports local or URL.

## Synopsis

```bash
toolbox video to-gif [INPUT_FILE] [-o PATH] [-fps INTEGER] [-w INTEGER] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox video to-gif <input_file>
toolbox video to-gif -o <output> -fps <fps> <input_file>
```

## Help

```text
Usage: toolbox video to-gif [OPTIONS] [INPUT_FILE]

  Convert video to GIF. Supports local or URL.

Options:
  -o, --output PATH    Output filename
  -fps, --fps INTEGER  Frames per second
  -w, --width INTEGER  GIF width
  --dry-run            Show what would happen
  --glob TEXT          Glob pattern to process
                       multiple files (e.g. '*.jpg')
  --parallel           Enable parallel processing
                       for batch operations
  --workers INTEGER    Number of worker threads
                       (default: CPU count)
  --help               Show this message and exit.
```

Parent: [toolbox video](Command-video)
Back: [Command Index](Command-Index)
