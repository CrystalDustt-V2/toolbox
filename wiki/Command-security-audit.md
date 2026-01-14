# toolbox security audit

Audit a file or directory for PII (Personally Identifiable Information).

Source: [src/toolbox/plugins/security/__init__.py:L54](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/security/__init__.py#L54)

## Synopsis

```bash
toolbox security audit PATH [--type [text|pdf|auto]]
```

## Examples

```bash
toolbox security audit <path>
toolbox security audit --type <file_type> <path>
```

## Help

```text
Usage: toolbox security audit [OPTIONS] PATH

  Audit a file or directory for PII (Personally
  Identifiable Information).

Options:
  --type [text|pdf|auto]
  --help                  Show this message and
                          exit.
```

Parent: [toolbox security](Command-security)
Back: [Command Index](Command-Index)
