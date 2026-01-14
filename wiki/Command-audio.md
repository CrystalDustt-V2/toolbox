# toolbox audio

Audio processing tools (requires FFmpeg).

## Subcommands

- [toolbox audio convert](Command-audio-convert) — Convert audio format (e.g., audio.wav audio.mp3). Supports local or URL.
- [toolbox audio merge](Command-audio-merge) — Merge multiple audio files into one. Supports local or URL.
- [toolbox audio normalize](Command-audio-normalize) — Normalize audio volume using loudnorm filter. Supports local or URL.
- [toolbox audio stt](Command-audio-stt) — Transcribe audio to text using OpenAI Whisper.
- [toolbox audio trim](Command-audio-trim) — Trim an audio file. Supports local or URL.

## Help

```text
Usage: toolbox audio [OPTIONS] COMMAND [ARGS]...

  Audio processing tools (requires FFmpeg).

Options:
  --help  Show this message and exit.

Commands:
  convert    Convert audio format (e.g.,...
  merge      Merge multiple audio files into one.
  normalize  Normalize audio volume using...
  stt        Transcribe audio to text using...
  trim       Trim an audio file.
```

Back: [Command Index](Command-Index)
