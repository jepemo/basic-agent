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

PID_CHILD = None

async def agent2(ctx):
    global PID_CHILD
    PID_CHILD = await ctx.start(agent1)

async def agent1(ctx):
    pass

class TestAgents(unittest.TestCase):
    def test_simple(self):
        pid = None
        with get_agent_context() as ctx:
            pid = ctx.start(agent1)
        self.assertEqual(pid, '0-1')

    def test_pid_child(self):
        global PID_CHILD
        with get_agent_context() as ctx:
            ctx.start(agent2)
        self.assertEqual(PID_CHILD, '0-1-1')
