# -*- coding: utf-8 -*-
# This file is part of bagent
#
# Copyright (C) 2018-present Jeremies Pérez Morata
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

from bagent import *

async def agent(ctx):
    (sender, msg) = await ctx.recv()
    await ctx.send(sender, "Hello {0}".format(msg))

async def main(ctx):
    pid = await ctx.start(agent)

    await ctx.send(pid, "Hello World")
    (_, msg) = await ctx.recv()
    print(msg)

with get_agent_context(debug=True) as ctx:
    ctx.start(main)
