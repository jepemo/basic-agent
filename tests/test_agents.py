import unittest

from bagent import *

async def agent1(ctx):
    pass

class TestAgents(unittest.TestCase):
    def test_simple(self):
        with get_agent_context() as ctx:
            pid = ctx.start(agent1)
            self.assertEqual(pid, '0-1')
