from aioagent import *

async def upper(text):
    return text.upper()

async def concat_and_up(ctx, *args):
    res = ""
    for t in args:
        res += await upper(t) + " "

    print(res.strip())

with get_agent_context() as ctx:
    ctx.run(concat_and_up, "hello", "world")
