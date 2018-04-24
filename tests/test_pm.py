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

MSG_TYPE_STR=None
MSG_TYPE_INT=None
MSG_TYPE_FLOAT=None
MSG_TYPE_RE=None

async def receiver(ctx):
    global MSG_TYPE_STR
    global MSG_TYPE_INT
    global MSG_TYPE_FLOAT
    global MSG_TYPE_RE
    while True:
        async with ctx.get_message() as m:
            if m.is_int():
                MSG_TYPE_INT = m.msg
            elif m.is_float():
                MSG_TYPE_FLOAT = m.msg
            elif m.is_re("EXIT"):
                MSG_TYPE_RE = m.msg
                break
            elif m.is_str():
                MSG_TYPE_STR = m.msg

async def sender(ctx):
    pid = await ctx.start(receiver)
    await ctx.send(pid, 1)
    await ctx.send(pid, 1.2)
    await ctx.send(pid, "mystring")
    await ctx.send(pid, "EXIT")

class TestPatternMatching(unittest.TestCase):
    def test_primitive_cases(self):
        with get_agent_context() as ctx:
            ctx.start(sender)

        self.assertEqual(MSG_TYPE_STR, "mystring")
        self.assertEqual(MSG_TYPE_INT, 1)
        self.assertEqual(MSG_TYPE_FLOAT, 1.2)
        self.assertEqual(MSG_TYPE_RE, "EXIT")
