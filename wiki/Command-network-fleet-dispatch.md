# toolbox network fleet-dispatch

Dispatch a ToolBox command to a remote worker node.

Source: [src/toolbox/plugins/network/__init__.py:L551](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/network/__init__.py#L551)

## Synopsis

```bash
toolbox network fleet-dispatch NODE_IP COMMAND [-p INTEGER]
```

## Examples

```bash
toolbox network fleet-dispatch <node_ip> <command>
toolbox network fleet-dispatch -p <port> <node_ip> <command>
```

## Help

```text
Usage: toolbox network fleet-dispatch 
           [OPTIONS] NODE_IP COMMAND

  Dispatch a ToolBox command to a remote worker
  node.

Options:
  -p, --port INTEGER
  --help              Show this message and exit.
```

Parent: [toolbox network](Command-network)
Back: [Command Index](Command-Index)
