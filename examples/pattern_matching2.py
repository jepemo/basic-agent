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

async def agent_sender(ctx, pid_receiver):
    await ctx.send(pid_receiver, 1)
    await ctx.send(pid_receiver, "hello")
    await ctx.send(pid_receiver, "12345")
    await ctx.send(pid_receiver, 1.2)
    await ctx.send(pid_receiver, "EXIT")

async def receiver(ctx):
    await ctx.start(agent_sender, ctx.pid)

    while True:
        async with ctx.get_message() as m:
            m.match_int(lambda x: print("Integer value:", x))
            m.match_re('[0-9]+', lambda x: print("RE:", x))
            if m.is_re("EXIT"):
                break
            m.match_str(lambda x: print("String value:", x))
            m.match_float(lambda x: print("Float value:", x))

with get_agent_context(debug=True) as ctx:
    pid_receiver = ctx.start(receiver)
