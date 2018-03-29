# aio-agent
Minimal &amp; Simple Agent Engine for Python

## Getting started

```bash
pip install aioagent
```

## Example

```python
from aioagent import *

@agent
def echo_upper():
  with get_message() as (sender, msg):
      send(sender, msg.upper())
      
p = echo_upper()

await send(p, "Hello World")
print(await recv())
```
