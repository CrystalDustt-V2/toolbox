# toolbox audio stt

Transcribe audio to text using OpenAI Whisper.

Source: [src/toolbox/plugins/audio/__init__.py:L25](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/audio/__init__.py#L25)

## Synopsis

```bash
toolbox audio stt INPUT_FILE [-m TEXT] [-o PATH] [--gpu]
```

## Examples

```bash
toolbox audio stt <input_file>
toolbox audio stt -m <model> -o <output> <input_file>
```

## Help

```text
Usage: toolbox audio stt [OPTIONS] INPUT_FILE

  Transcribe audio to text using OpenAI Whisper.

Options:
  -m, --model TEXT   Whisper model size (tiny, base,
                     small, medium, large)
  -o, --output PATH  Output text file
  --gpu              Use GPU for inference
  --help             Show this message and exit.
```

Parent: [toolbox audio](Command-audio)
Back: [Command Index](Command-Index)
