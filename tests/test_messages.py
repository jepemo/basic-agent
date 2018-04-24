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
import unittest
from bagent import *

MSG_RECEIVED1 = None
MSG_RECEIVED2 = None

async def agent1a(ctx):
    pid = await ctx.start(agent1b)
    await ctx.send(pid, "msg1")

async def agent1b(ctx):
    global MSG_RECEIVED1
    (sender, msg) = await ctx.recv()
    MSG_RECEIVED1 = msg

async def agent2a(ctx):
    pid = await ctx.start(agent2b)
    await ctx.send(pid, "msg2")

async def agent2b(ctx):
    global MSG_RECEIVED2
    async with ctx.get_message() as m:
        MSG_RECEIVED2 = m.msg

class TestMessages(unittest.TestCase):
    def test_recv(self):
        with get_agent_context() as ctx:
            ctx.start(agent1a)
        self.assertEqual(MSG_RECEIVED1, "msg1")

    def test_get_message(self):
        with get_agent_context() as ctx:
            ctx.start(agent2a)
        self.assertEqual(MSG_RECEIVED2, "msg2")
