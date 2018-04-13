from aioagent import *

async def hello(text):
    print("Hello", text)

async def parent():
    await hello("World")

run(parent)
