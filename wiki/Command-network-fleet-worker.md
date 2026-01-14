# toolbox network fleet-worker

Start a distributed worker to accept remote tasks.

Source: [src/toolbox/plugins/network/__init__.py:L424](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/network/__init__.py#L424)

## Synopsis

```bash
toolbox network fleet-worker [-p INTEGER] [--name TEXT]
```

## Examples

```bash
toolbox network fleet-worker -p <port> --name <name>
```

## Help

```text
Usage: toolbox network fleet-worker 
           [OPTIONS]

  Start a distributed worker to accept remote tasks.

Options:
  -p, --port INTEGER  Port for the task listener
  --name TEXT         Name for this node
  --help              Show this message and exit.
```

Parent: [toolbox network](Command-network)
Back: [Command Index](Command-Index)
