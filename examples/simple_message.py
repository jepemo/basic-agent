from bagent import *

async def agent(ctx):
    (sender, msg) = await ctx.get_message()
    await ctx.send(sender, "Hello {0}".format(msg))

async def main(ctx):
    pid = ctx.run(agent)

    await ctx.send(pid, "Hello World")
    (_, msg) = await ctx.get_message()
    print(msg)

with get_agent_context(debug=True) as ctx:
    ctx.run(main)
