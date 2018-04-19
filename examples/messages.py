from aioagent import *

async def server():
    pass

async def client(msg):
    print(msg)

with get_agent_context() as ctx:
    ctx.run(server)

    for i in range(0, 5):
        ctx.run(client, i)
