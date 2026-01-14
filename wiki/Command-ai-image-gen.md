# toolbox ai image-gen

Generate an image from text using local Stable Diffusion (ONNX).

Source: [src/toolbox/plugins/ai/__init__.py:L148](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/ai/__init__.py#L148)

## Synopsis

```bash
toolbox ai image-gen PROMPT [-o TEXT] [--steps INTEGER]
```

## Examples

```bash
toolbox ai image-gen <prompt>
toolbox ai image-gen -o <output> --steps <steps> <prompt>
```

## Help

```text
Usage: toolbox ai image-gen [OPTIONS] PROMPT

  Generate an image from text using local Stable
  Diffusion (ONNX).

Options:
  -o, --output TEXT  Output filename
  --steps INTEGER    Inference steps
  --help             Show this message and exit.
```

Parent: [toolbox ai](Command-ai)
Back: [Command Index](Command-Index)
