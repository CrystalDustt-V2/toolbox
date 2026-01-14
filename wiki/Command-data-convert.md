# toolbox data convert

Convert between JSON, CSV, and YAML. Supports local or URL.

## Synopsis

```bash
toolbox data convert [INPUT_FILE] [--from-format [json|csv|yaml]] [--to-format [json|csv|yaml]] [-o TEXT] [--dry-run] [--glob TEXT] [--parallel] [--workers INTEGER]
```

## Examples

```bash
toolbox data convert <input_file>
toolbox data convert --from-format <from_format> --to-format <to_format> <input_file>
```

## Help

```text
Usage: toolbox data convert [OPTIONS] [INPUT_FILE]

  Convert between JSON, CSV, and YAML. Supports
  local or URL.

Options:
  --from-format [json|csv|yaml]  Input format
  --to-format [json|csv|yaml]    Output format
                                 [required]
  -o, --output TEXT              Output filename
  --dry-run                      Show what would
                                 happen
  --glob TEXT                    Glob pattern to
                                 process multiple
                                 files (e.g.
                                 '*.jpg')
  --parallel                     Enable parallel
                                 processing for
                                 batch operations
  --workers INTEGER              Number of worker
                                 threads (default:
                                 CPU count)
  --help                         Show this message
                                 and exit.
```

Parent: [toolbox data](Command-data)
Back: [Command Index](Command-Index)
