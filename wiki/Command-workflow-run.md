# toolbox workflow run

Run a sequence of commands from a workflow YAML file.

Source: [src/toolbox/cli.py:L307](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/cli.py#L307)

## Synopsis

```bash
toolbox workflow run WORKFLOW_FILE [-v TEXT] [--dry-run] [--debug-workflow]
```

## Examples

```bash
toolbox workflow run <workflow_file>
toolbox workflow run -v <var> --dry-run <workflow_file>
```

## Help

```text
Usage: toolbox workflow run [OPTIONS] WORKFLOW_FILE

  Run a sequence of commands from a workflow YAML
  file.

Options:
  -v, --var TEXT    Override workflow variables
                    (key=value)
  --dry-run         Validate workflow without
                    executing commands
  --debug-workflow  Show detailed execution trace
                    for workflows
  --help            Show this message and exit.
```

Parent: [toolbox workflow](Command-workflow)
Back: [Command Index](Command-Index)
