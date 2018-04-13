# aio-agent
Minimal &amp; Simple Agent Engine for Python

## Getting started

```bash
pip install aioagent
```

## Example

```python
from aioagent import agent, run, send

@agent
async def echo_upper():
  with get_message() as (sender, msg):
      send(sender, msg.upper())

run()
```
