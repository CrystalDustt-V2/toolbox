# toolbox workflow watch

Watch a directory for new files and auto-trigger a workflow.

Source: [src/toolbox/cli.py:L365](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/cli.py#L365)

## Synopsis

```bash
toolbox workflow watch DIRECTORY WORKFLOW_FILE [--ext TEXT]
```

## Examples

```bash
toolbox workflow watch <directory> <workflow_file>
toolbox workflow watch --ext <ext> <directory> <workflow_file>
```

## Help

```text
Usage: toolbox workflow watch [OPTIONS] DIRECTORY
                              WORKFLOW_FILE

  Watch a directory for new files and auto-trigger a
  workflow.

Options:
  --ext TEXT  Extensions to watch for (e.g. .jpg)
  --help      Show this message and exit.
```

Parent: [toolbox workflow](Command-workflow)
Back: [Command Index](Command-Index)
