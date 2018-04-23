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

async def receiver(ctx):
    await ctx.start(agent_sender, ctx.pid)

    while True:
        async with ctx.get_message() as m:
            if m.is_int():
                print("Integer value:", m.msg)
            elif m.is_re('[0-9]+'):
                print("RE:", m.msg)
            elif m.is_str():
                print("String value:", m.msg)
            elif m.is_float():
                print("Float value:", m.msg)
                break

with get_agent_context(debug=True) as ctx:
    pid_receiver = ctx.start(receiver)
