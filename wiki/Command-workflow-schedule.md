# toolbox workflow schedule

Schedule a workflow to run periodically.

Source: [src/toolbox/cli.py:L406](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/cli.py#L406)

## Synopsis

```bash
toolbox workflow schedule WORKFLOW_FILE [--interval INTEGER] [--immediate]
```

## Examples

```bash
toolbox workflow schedule <workflow_file>
toolbox workflow schedule --interval <interval> --immediate <workflow_file>
```

## Help

```text
Usage: toolbox workflow schedule 
           [OPTIONS] WORKFLOW_FILE

  Schedule a workflow to run periodically.

Options:
  --interval INTEGER  Interval in minutes
  --immediate         Run immediately before first
                      interval
  --help              Show this message and exit.
```

Parent: [toolbox workflow](Command-workflow)
Back: [Command Index](Command-Index)
