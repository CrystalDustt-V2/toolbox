# toolbox util workflow

Run a YAML workflow with dynamic logic (if/else, variables).

Source: [src/toolbox/plugins/util/__init__.py:L225](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/util/__init__.py#L225)

## Synopsis

```bash
toolbox util workflow WORKFLOW_FILE [--vars TEXT]
```

## Examples

```bash
toolbox util workflow <workflow_file>
toolbox util workflow --vars <vars> <workflow_file>
```

## Help

```text
Usage: toolbox util workflow [OPTIONS] WORKFLOW_FILE

  Run a YAML workflow with dynamic logic (if/else,
  variables).

Options:
  --vars TEXT  Variables for the workflow
               (key=value)
  --help       Show this message and exit.
```

Parent: [toolbox util](Command-util)
Back: [Command Index](Command-Index)
