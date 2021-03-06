# basic-agent
Minimal &amp; Simple Agent Engine for Python

[![Build Status](https://travis-ci.org/jepemo/basic-agent.svg?branch=master)](https://travis-ci.org/jepemo/basic-agent)

- [Getting started](#getting-started)
- [Features](#features)
- [Documentation](#documentation)
  - [Agent creation](#agent-creation)
  - [Message passing](#message-passing)
  - [Pattern matching](#pattern-matching)


## Getting started

### Installation

```bash
pip install bagent
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

For the *message context* you need the agent context:

```python
async def slave(ctx):
    async with ctx.get_message() as m:
        print("Message {0} received from {1}".format(m.msg, m.sender))
```


### Pattern matching

When you receive a message with the *message context* you can use it to facilitate the message processing. This provides several pattern-matching utilities.

The most simple are the type checkers:
 - is_str : Check if the message is a string
 - is_float : Check if the message is a float
 - is_int : Check if the message is an integer
 - is_type(type T) : Check if the message is from type T
 - is_re(re string) : Check if the message matches with the regular expresion string.

For example:
```python

async def slave(ctx):
  async with get_message() as m:
    if m.is_int():
      print("It's an integer")
    elif m.is_float():
      print("It's a float")

async def master(ctx):
  pid = await ctx.start(slave)
  await ctx.send(pid, 1.2)
```

One tipical pattern is to have al infinite loop inside the agent and finish it with one type of message:

```python
async def slave(ctx):
  while True:
    async with get_message() as m:
      if m.is_re("EXIT"):
        break
      else:
        print(m.msg)

async def master(ctx):
  pid = await ctx.start(slave)
  await ctx.send(pid, 1)
  await ctx.send(pid, 2)
  await ctx.send(pid, 3)
  await ctx.send(pid, "EXIT")

# Exit:
# 1
# 2
# 3
```

## TODO & Ideas:
  - Improvements agent context strategies:
    - Timeout for cancel all agents
    - Timetout warns agent is taking too much time.
    - Strategy waits until all agents ends (actual strategy, default)
    - Strategy cancel other agents when first finishes.
  - Benchmark
  - Improve loop management
    - Creating specialized agent?
    ```python3
    @AgentReceiver
    async def receiver(ctx, msg_handler):
      # ...
      msg_handler.exit()
    ```
  - Create especialized agent_context for an http/tcp server
    - Every agent is a request
  - Run code after the context depending of the state (error, strategy?)
  - Delay starting agent (timeout param)
  - Publish/Suscribe messaging model?
  - Timeout in recv
  - Shared (inmutable) data for an agent subtree (with a dictionary)?
  - HA/Resilient strategies for failed agents?
