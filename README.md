# HYPERLOG

AI Terminal for Samsung S24 / Termux - Powered by Venice AI

```
    ██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██╗      ██████╗  ██████╗
    ██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║     ██╔═══██╗██╔════╝
    ███████║ ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║     ██║   ██║██║  ███╗
    ██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ██╔══██╗██║     ██║   ██║██║   ██║
    ██║  ██║   ██║   ██║     ███████╗██║  ██║███████╗╚██████╔╝╚██████╔╝
    ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝
```

## Features

- Animated cyberpunk intro
- Multiple AI models (Llama 3.3 70B, DeepSeek R1, Uncensored, etc.)
- Streaming responses
- Clean mobile-optimized UI
- Venice AI API integration

## Install

```bash
# Termux
pkg install python
pip install requests

# Download
curl -o ~/bin/hyperlog https://raw.githubusercontent.com/nattimmis/venice-cli/main/hyperlog.py
chmod +x ~/bin/hyperlog
```

## Usage

```bash
hyperlog        # Full animated intro
hyperlog -f     # Fast launch (skip intro)
```

## Commands

| Command | Description |
|---------|-------------|
| `/m` | Switch model |
| `/w` | Toggle web search |
| `/t 0.8` | Set temperature (0-2) |
| `/s` | Set system prompt |
| `/n` | New conversation |
| `/c` | Clear screen |
| `/h` | Help |
| `/q` | Quit |

## Models

1. **GLM-4** - General purpose
2. **Uncensored** - Dolphin Mistral (no filters)
3. **Medium** - Mistral 31 24B
4. **DeepSeek R1** - Reasoning model
5. **Llama 3.3 70B** - Default, best quality

## API

Uses Venice AI API. Get your key at [venice.ai](https://venice.ai)

## License

MIT
