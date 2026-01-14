# toolbox ai chat

Chat with a local LLM (offline, supports RAG).

Source: [src/toolbox/plugins/ai/__init__.py:L45](https://github.com/CrystalDustt-V2/toolbox/blob/master/src/toolbox/plugins/ai/__init__.py#L45)

## Synopsis

```bash
toolbox ai chat PROMPT [--model TEXT] [--rag] [--max-tokens INTEGER]
```

## Examples

```bash
toolbox ai chat <prompt>
toolbox ai chat --model <model> --rag <prompt>
```

## Help

```text
Usage: toolbox ai chat [OPTIONS] PROMPT

  Chat with a local LLM (offline, supports RAG).

Options:
  --model TEXT          LLM model to use
  --rag                 Use indexed documents for
                        context
  --max-tokens INTEGER  Max tokens to generate
  --help                Show this message and exit.
```

Parent: [toolbox ai](Command-ai)
Back: [Command Index](Command-Index)
