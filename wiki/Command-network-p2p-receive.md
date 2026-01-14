# toolbox network p2p-receive

Receive a file from another ToolBox instance.

Source: [src/toolbox/plugins/network/__init__.py:L236](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/network/__init__.py#L236)

## Synopsis

```bash
toolbox network p2p-receive HOST [-p INTEGER] [--password TEXT] [-o TEXT]
```

## Examples

```bash
toolbox network p2p-receive <host>
toolbox network p2p-receive -p <port> --password <password> <host>
```

## Help

```text
Usage: toolbox network p2p-receive 
           [OPTIONS] HOST

  Receive a file from another ToolBox instance.

Options:
  -p, --port INTEGER  Port to connect to
  --password TEXT     Password for decryption
  -o, --output TEXT   Output directory
  --help              Show this message and exit.
```

Parent: [toolbox network](Command-network)
Back: [Command Index](Command-Index)
