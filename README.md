# aio-agent
Minimal &amp; Simple Agent Engine for Python

## Getting started

```bash
pip install aioagent
```

## Example

```python
from aioagent import *

async def echo_upper():
    with get_message() as (sender, msg):
        if match(msg, ("upper", quote(text))):
            send(sender, text.upper())
        elif match(msg, ("lower", quote(text))):
            send(sender, text.lower())

run(echo_upper)
```

Mirar: https://docs.python.org/3/library/contextlib.html
