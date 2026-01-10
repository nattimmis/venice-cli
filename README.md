# Hyperlog

Venice AI CLI client for Termux/Android.

## Features

- Clean, compact UI for mobile screens
- Multiple AI models (GLM-4, Venice Uncensored, Venice Medium)
- Web search integration
- Streaming responses
- Login/logout support
- Session persistence

## Install

```bash
# Termux
pkg install python
pip install requests

# Download and install
curl -o ~/bin/hyperlog https://raw.githubusercontent.com/hyperlogic/hyperlog/main/hyperlog.py
chmod +x ~/bin/hyperlog
```

## Usage

```bash
hyperlog
```

## Commands

| Command | Description |
|---------|-------------|
| `/h` | Help |
| `/m` | Change model |
| `/w` | Toggle web search |
| `/t 0.8` | Set temperature |
| `/s` | Set system prompt |
| `/n` | New conversation |
| `/c` | Clear screen |
| `/login` | Login with email |
| `/logout` | Logout |
| `/status` | Show login status |
| `/q` | Quit |

## Models

1. **GLM-4** - Default model
2. **Venice Uncensored 1.1** - Uncensored Dolphin model
3. **Venice Medium** - Mistral-based model

## License

MIT
