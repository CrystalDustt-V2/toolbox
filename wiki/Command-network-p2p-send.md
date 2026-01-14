# toolbox network p2p-send

Send a file to another ToolBox instance on the network.

Source: [src/toolbox/plugins/network/__init__.py:L148](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/network/__init__.py#L148)

## Synopsis

```bash
toolbox network p2p-send INPUT_FILE [-p INTEGER] [--password TEXT]
```

## Examples

```bash
toolbox network p2p-send <input_file>
toolbox network p2p-send -p <port> --password <password> <input_file>
```

## Help

```text
Usage: toolbox network p2p-send [OPTIONS] INPUT_FILE

  Send a file to another ToolBox instance on the
  network.

Options:
  -p, --port INTEGER  Port to listen on
  --password TEXT     Password for encryption
  --help              Show this message and exit.
```

Parent: [toolbox network](Command-network)
Back: [Command Index](Command-Index)
