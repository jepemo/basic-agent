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
from bagent import *

async def slave(ctx):
    print("start slave and waiting 5 secs")
    await asyncio.sleep(5)

async def master(ctx):
    print("start master")
    await ctx.start(slave)

with get_agent_context(debug=True) as ctx:
    ctx.start(master)
