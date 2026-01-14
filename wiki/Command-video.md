# toolbox video

Video processing tools (requires FFmpeg).

## Subcommands

- [toolbox video compress](Command-video-compress) — Compress video using H.264. Supports local or URL.
- [toolbox video extract-audio](Command-video-extract-audio) — Extract audio from a video file. Supports local or URL.
- [toolbox video extract-frames](Command-video-extract-frames) — Extract frames from video at intervals. Supports local or URL.
- [toolbox video remove-watermark](Command-video-remove-watermark) — Remove a watermark from a specific area using the delogo filter.
- [toolbox video to-gif](Command-video-to-gif) — Convert video to GIF. Supports local or URL.
- [toolbox video to-sticker](Command-video-to-sticker) — Convert a video to a sticker. Supports local or URL.
- [toolbox video trim](Command-video-trim) — Trim a video file. Supports local or URL.
- [toolbox video upscale](Command-video-upscale) — Upscale video using AI (ESRGAN). WARNING: Very slow and resource-intensive.
- [toolbox video watermark](Command-video-watermark) — Add text or image watermark to a video.

## Help

```text
Usage: toolbox video [OPTIONS] COMMAND [ARGS]...

  Video processing tools (requires FFmpeg).

Options:
  --help  Show this message and exit.

Commands:
  compress          Compress video using H.264.
  extract-audio     Extract audio from a video...
  extract-frames    Extract frames from video...
  remove-watermark  Remove a watermark from a...
  to-gif            Convert video to GIF.
  to-sticker        Convert a video to a sticker.
  trim              Trim a video file.
  upscale           Upscale video using AI...
  watermark         Add text or image watermark...
```

Back: [Command Index](Command-Index)
