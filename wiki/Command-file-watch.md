# toolbox file watch

Watch a directory for changes and trigger a ToolBox command.

Source: [src/toolbox/plugins/file/__init__.py:L290](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/file/__init__.py#L290)

## Synopsis

```bash
toolbox file watch DIRECTORY [--command TEXT] [--recursive]
```

## Examples

```bash
toolbox file watch <directory>
toolbox file watch --command <command> --recursive <directory>
```

## Help

```text
Usage: toolbox file watch [OPTIONS] DIRECTORY

  Watch a directory for changes and trigger a
  ToolBox command.

Options:
  --command TEXT  ToolBox command to run on change
  --recursive     Watch recursively
  --help          Show this message and exit.
```

Parent: [toolbox file](Command-file)
Back: [Command Index](Command-Index)
