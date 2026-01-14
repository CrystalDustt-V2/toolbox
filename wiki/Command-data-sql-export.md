# toolbox data sql-export

Export JSON or CSV data to a SQLite database.

Source: [src/toolbox/plugins/data/__init__.py:L126](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/data/__init__.py#L126)

## Synopsis

```bash
toolbox data sql-export INPUT_FILE [-d TEXT] [-t TEXT] [--dry-run]
```

## Examples

```bash
toolbox data sql-export <input_file>
toolbox data sql-export -d <db> -t <table> <input_file>
```

## Help

```text
Usage: toolbox data sql-export [OPTIONS] INPUT_FILE

  Export JSON or CSV data to a SQLite database.

Options:
  -d, --db TEXT     Target SQLite database file
  -t, --table TEXT  Target table name
  --dry-run         Show what would happen
  --help            Show this message and exit.
```

Parent: [toolbox data](Command-data)
Back: [Command Index](Command-Index)
