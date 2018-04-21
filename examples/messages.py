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

MAX_REQUESTS = 5

async def server(ctx):
    counter = 0
    while counter < MAX_REQUESTS:
        (sender, msg) = await ctx.recv()
        print("Received:", msg, "from", sender)
        counter += 1
    print("Finishing server...")

async def client(ctx, pid_server, msg):
    await ctx.send(pid_server, msg)

with get_agent_context(debug=False) as ctx:
    pid_server = ctx.start(server)

    for i in range(0, MAX_REQUESTS):
        ctx.start(client, pid_server, i)
