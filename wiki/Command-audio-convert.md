# toolbox audio convert

Convert audio format (e.g., audio.wav audio.mp3). Supports local or URL.

Source: [src/toolbox/plugins/audio/__init__.py:L62](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/audio/__init__.py#L62)

## Synopsis

```bash
toolbox audio convert INPUT_FILE OUTPUT_FILE [--dry-run]
```

## Examples

```bash
toolbox audio convert <input_file> <output_file>
toolbox audio convert --dry-run <input_file> <output_file>
```

## Help

```text
Usage: toolbox audio convert [OPTIONS] INPUT_FILE
                             OUTPUT_FILE

  Convert audio format (e.g., audio.wav audio.mp3).
  Supports local or URL.

Options:
  --dry-run  Show what would happen
  --help     Show this message and exit.
```

Parent: [toolbox audio](Command-audio)
Back: [Command Index](Command-Index)
