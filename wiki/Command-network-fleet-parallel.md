# toolbox network fleet-parallel

Hyper-Scale Parallelism: Split a batch of files across all fleet nodes.

Source: [src/toolbox/plugins/network/__init__.py:L623](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/network/__init__.py#L623)

## Synopsis

```bash
toolbox network fleet-parallel [FILES]... [--cmd TEXT] [--timeout INTEGER]
```

## Examples

```bash
toolbox network fleet-parallel <files>...
toolbox network fleet-parallel --cmd <cmd> --timeout <timeout> <files>...
```

## Help

```text
Usage: toolbox network fleet-parallel 
           [OPTIONS] [FILES]...

  Hyper-Scale Parallelism: Split a batch of files
  across all fleet nodes.

Options:
  --cmd TEXT         Command to run on each file
                     (use {} for filename)
                     [required]
  --timeout INTEGER  Discovery timeout
  --help             Show this message and exit.
```

Parent: [toolbox network](Command-network)
Back: [Command Index](Command-Index)
