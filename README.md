# basic-agent
Minimal &amp; Simple Agent Engine for Python

## Getting started

### Installation

```bash
# Not yet: pip install bagent
```

## Example

```python
from bagent import *

async def slave(ctx):
    with ctx.get_message() as m:
        if m.is_str():
            print(m.msg)

async def master(ctx):
    slave_pid = ctx.start(slave)
    ctx.send(slave_pid, "Hello World")

with get_agent_context() as ctx:
    ctx.start(master)
```

## Features
- **asyncio** integration
- Simple message passing model
- Simple-pattern matching

## Documentation

### Agent creation
You can create agents like python3 async functions.

First of all you need to create the root context, and start the first level processes inside. This processes can be started in any order.
For example:

```python
from bagent import *

async def agent1(ctx, param1):
    print(param1)

with get_agent_context() as ctx:
    for i in range(0, 4):
        ctx.start(agent1, i)

# Result:
# 0
# 3
# 1
# 2
```

An agent is defined like an *async function*. The only requirement is that the first parameter is the *agent context*. This context is used to start another agents, send messages to them and use the pattern matching.

And of course, you can use async functions inside an agent:

```python
from bagent import *

async slave(ctx):
    await asyncio.sleep(1)

async master(ctx):
    ctx.start(slave)

with get_agent_context() as ctx:
    ctx.start(master)
```

### Message passing

### Pattern matching

## Benchmark

TODO
