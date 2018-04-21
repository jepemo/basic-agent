# basic-agent
Minimal &amp; Simple Agent Engine for Python

## Getting started

```bash
# Not yet: pip install bagent
```

## Example

```python
from bagent import *

async def agent1(ctx, msg):
    print(msg)

with get_agent_context() as ctx:
    ctx.start(agent1, "Hello World")
```

## Features
- **asyncio** integration
- Simple message passing model


## TODO
  - Send/recv messages from root context
  - Simple-pattern matching
  - Benchmarks

