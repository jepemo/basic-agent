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

import asyncio
import time
from bagent import *

NUM_ITERATIONS=3

async def slave(ctx):
    (sender, msg) = await ctx.recv()
    await ctx.send(sender, "PONG")

async def master(ctx, num_procs):
    for i in range(num_procs):
        pid = await ctx.start(slave)
        await ctx.send(pid, "PING")
        await ctx.recv()

for i in [1, 10, 100, 1000, 10000, 100000]:
    ini = time.time()
    for j in range(0, NUM_ITERATIONS):
        with get_agent_context(debug=False) as ctx:
            ctx.start(master, i)
    end = (time.time() - ini) / NUM_ITERATIONS
    time.sleep(1)
    print("For {0} takes {1} seconds".format(i, end))
