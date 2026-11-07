# Free-ZAI-Api

![Preview in terminal](image.png)


Self-hosted OpenAI-compatible API proxy for [chat.z.ai](https://chat.z.ai) (GLM-5.3 / GLM-5.2 / etc).
Runs a real browser session via **Playwright**, so the site sees a genuine Chrome fingerprint — the invisible Aliyun captcha passes automatically.

> Built for use with [opencode](https://opencode.ai) and any other OpenAI-compatible client.

## Install

```bash
git clone https://github.com/lothiann/Free-ZAI-Api.git
cd Free-ZAI-Api
pip install -r requirements.txt
playwright install chromium
```

## Get the token

Open https://chat.z.ai → DevTools (`F12`) → Console:

```js
fetch('/api/v1/auths/').then(r=>r.json()).then(d=>window.__acc={id:d.id,email:d.email,name:d.name,token:d.token})
```
```js
copy(JSON.stringify(__acc))
```

Paste into `accounts.json`:

```json
{
  "rotate_every": 10,
  "accounts": [
    { "name": "main", "email": "you@gmail.com", "token": "eyJ..." }
  ]
}
```

| Field | Description |
|---|---|
| `token` | JWT from DevTools (**required**) |
| `rotate_every` | requests per account before switching to the next one |

Accounts rotate round-robin — add more than one to spread load and survive a dead token.

## Run

```bash
python main.py
```

Server starts on `http://127.0.0.1:8492/v1`.

## Custom Terminal Client (Added in this Fork)

This fork includes an additional script — **`chat_client.py`** — designed for users who want to chat with the models directly from their terminal without installing third-party GUI clients (like opencode or Chatbox).

### Features
- **Conversation Memory**: Unlike basic scripts, this client stores the chat history, so the model remembers previous messages.
- **System Prompt Support**: You can define the model's persona (e.g., "You are a senior Python developer") right in the code.
- **Zero Configuration**: Works out of the box as long as the main server (`main.py`) is running.

### How to use

1. **Start the server** in the first terminal window:
   ```bash
   python main.py
   ```

2. Install the OpenAI library (if you haven't already):
   ```bash
   pip install openai
   ```

3. Run the custom client in a second terminal window:
   ```bash
   python chat.py
   ```

4. Chat! The script will prompt you for input. Type exit to quit.

### Customization
You can edit the SYSTEM_PROMPT variable inside chat_client.py to change the model's behavior. For example:
```python
SYSTEM_PROMPT = "ur prompt"
```

### The Script (chat.py)
If you prefer to copy the code manually, here it is:
```python
from openai import OpenAI

MODEL_NAME = "x-preview-l" 

SYSTEM_PROMPT = "ur prompt"

client = OpenAI(base_url="http://127.0.0.1:8492/v1", api_key="sk-nothing")

messages = []

if SYSTEM_PROMPT:
    messages.append({"role": "system", "content": SYSTEM_PROMPT})

print(f"chat from {MODEL_NAME} has started.")
print(f"sys prompt: {SYSTEM_PROMPT}")
print("write answer (exit from exit):")

while True:
    q = input("\nYou: ")
    if q.lower() == "exit":
        break
    
    messages.append({"role": "user", "content": q})
    
    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )
        
        answer = resp.choices[0].message.content
        print(f"GLM: {answer}")
        
        messages.append({"role": "assistant", "content": answer})
        
    except Exception as e:
        print(f"\n[Error]: {e}")
        messages.pop()
```

### Test

```bash
curl http://127.0.0.1:8492/v1/models

curl -N http://127.0.0.1:8492/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d "{\"model\":\"glm-5.2\",\"stream\":true,\"messages\":[{\"role\":\"user\",\"content\":\"say OK\"}]}"

# account status
curl http://127.0.0.1:8492/accounts
```

## opencode

Add to `~/.config/opencode/opencode.jsonc` (or `opencode.json`):

```jsonc
{
  "provider": {
    "zai": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Z.AI (browser proxy)",
      "options": {
        "baseURL": "http://127.0.0.1:8492/v1",
        "apiKey": "sk-nothing"
      },
      "models": {
        "glm-5.3": { "name": "GLM-5.3", "limit": { "context": 2000000, "output": 2000000 } },
        "x-preview-l": { "name": "GLM-5.3 Flash", "limit": { "context": 2000000, "output": 2000000 } },
        "glm-5.2": { "name": "GLM-5.2", "limit": { "context": 2000000, "output": 2000000 } },
        "GLM-5-Turbo": { "name": "GLM-5 Turbo", "limit": { "context": 2000000, "output": 2000000 } },
        "GLM-5v-Turbo": { "name": "GLM-5v Turbo", "limit": { "context": 2000000, "output": 2000000 } },
        "glm-4.7": { "name": "GLM-4.7", "limit": { "context": 2000000, "output": 2000000 } },
        "glm-4.6v": { "name": "GLM-4.6v", "limit": { "context": 2000000, "output": 2000000 } },
        "GLM-4.1V-Thinking-FlashX": { "name": "GLM-4.1V Thinking FlashX", "limit": { "context": 2000000, "output": 2000000 } },
        "deep-research": { "name": "Deep Research", "limit": { "context": 2000000, "output": 2000000 } },
        "zero": { "name": "Zero", "limit": { "context": 2000000, "output": 2000000 } },
        "0727-106B-API": { "name": "0727 106B API", "limit": { "context": 2000000, "output": 2000000 } },
        "0727-360B-API": { "name": "0727 360B API", "limit": { "context": 2000000, "output": 2000000 } },
        "0808-360B-DR": { "name": "0808 360B DR", "limit": { "context": 2000000, "output": 2000000 } },
        "glm-4-flash": { "name": "GLM-4 Flash", "limit": { "context": 2000000, "output": 2000000 } },
        "glm-4-air-250414": { "name": "GLM-4 Air", "limit": { "context": 2000000, "output": 2000000 } }
      }
    }
  }
}
```

`apiKey` is ignored — the proxy binds to `127.0.0.1` and does not check it.

## Endpoints

| Endpoint | Description |
|---|---|
| `GET /v1/models` | model list parsed from the site |
| `POST /v1/chat/completions` | chat, streaming & non-streaming, with tools |
| `GET /accounts` | rotation status |

## Notes

- Tool calling works out of the box: send standard OpenAI `tools`, results come back as `role: "tool"` messages — nothing to configure.
- Reasoning is streamed via `delta.reasoning_content`, the answer via `delta.content`.
- `usage` counts **characters**, matching the site's ~2M limit — the `limit` values in the config above account for that.
- Logs are written to `logs/`, the last raw response to `last_response.json`.

## Disclaimer

For personal / educational use. Automating chat.z.ai may violate its Terms of Service — use your own accounts at your own risk.
