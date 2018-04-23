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
    async with ctx.get_message() as m:
        if m.is_str():
            print(m.msg)

async def master(ctx):
    slave_pid = await ctx.start(slave)
    await ctx.send(slave_pid, "Hello World")

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
    await ctx.start(slave)

with get_agent_context() as ctx:
    ctx.start(master)
```

### Message passing

When you start an agent it's PID is returned, so you can use it to send it messages. You can only send messages inside an agent, not in the root context.

```python
async def slave(ctx):
    (sender, msg) = await ctx.recv()
    await ctx.send(sender, "PONG")

async def master(ctx):
    pid = ctx.start(slave)
    await pid.send(pid, "PING")
    (sender, msg) = await ctx.recv()
    print(msg)
```

There are two ways to receive a message. With the simple recv and with the *message context*. You can see recv case in the above example.

For the message context you need the agent context:

```
async def slave(ctx):
    async with ctx.get_message() as m:
        print("Message {0} received from {1}".format(m.msg, m.sender))
```


### Pattern matching

## Benchmark

TODO
