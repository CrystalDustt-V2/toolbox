# toolbox network mesh-sync

Global Mesh Sync: DHT-based synchronization for vaults across locations.

Source: [src/toolbox/plugins/network/__init__.py:L113](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/network/__init__.py#L113)

## Synopsis

```bash
toolbox network mesh-sync VAULT_PATH [--dht]
```

## Examples

```bash
toolbox network mesh-sync <vault_path>
toolbox network mesh-sync --dht <vault_path>
```

## Help

```text
Usage: toolbox network mesh-sync 
           [OPTIONS] VAULT_PATH

  Global Mesh Sync: DHT-based synchronization for
  vaults across locations.

Options:
  --dht   Use Global DHT for node discovery
  --help  Show this message and exit.
```

Parent: [toolbox network](Command-network)
Back: [Command Index](Command-Index)
