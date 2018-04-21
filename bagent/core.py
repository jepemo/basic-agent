# -*- coding: utf-8 -*-
# Minimal & Simple Agent Engine for Python
#
# Copyright (C) 2018-present Jeremies Pérez Morata
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import logging
from contextlib import ContextDecorator

logger = logging.getLogger(__name__)

class AgentMixin(object):
    def __init__(self, loop, debug):
        self.next_pid = 1
        self.parent_pid = 0
        self.agents = {}
        self.loop = loop
        self.debug = debug
        self.pid = 1
        self.messages = asyncio.Queue(loop=loop)

    def next_pid(self, parent_pid):
        self.next_pid += 1
        return '{0}-{1}'.format(self.parent_pid, self.next_pid)

    def create_agent(self, agent_fn, *args, **kwargs):
        agent = AgentContext(self.loop, debug=self.debug)

        pid = '{0}-{1}'.format(self.pid, self.next_pid)
        agent.parent_pid = self.pid
        agent.pid = pid
        agent.fn = agent_fn
        agent.args = args
        agent.kwargs = kwargs
        agent.parent_ctx = self

        logger.debug("Agent created: {0}".format(agent.pid))

        self.agents[pid] = agent

        return pid


class AgentContext(AgentMixin):
    def __init__(self, loop, debug=False):
        self.loop = loop
        self.agents = {}
        self.pid = 0
        self.parent_ctx = None
        self.parent_pid = 0
        self.next_pid = 1
        self.fn = None
        self.args = None
        self.kwargs = None
        self.messages = asyncio.Queue(loop=loop)
        self.debug = debug
        self.entered_context = False

    def run(self, agent_fn, *args, **kwargs):
        pid = self.create_agent(agent_fn, *args, **kwargs)

        if not self.entered_context:
            self.loop.run_until_complete(asyncio.wait([agent.execute()]))

        return pid

    async def execute(self):
        logger.debug("Starting agent: {0}".format(self.pid))
        await self.fn(self, *self.args, **self.kwargs)

    async def send(self, pid, msg, sender=None):
        if not sender:
            sender = self.pid

        logger.debug("From {0}, sending {1} to {2}".format(sender, str(msg), pid))

        if self.pid == pid:
            await self.messages.put((sender, msg))
        else:
            agent = self._find_child_path(pid)
            # Todo: if agent is None....
            await agent.send(pid, msg, sender=sender)

    def _find_child_path(self, pid):
        for apid, agent in self.agents.items():
            if apid.startswith(pid):
                return agent
        return None

    async def recv(self):
        return await self.messages.get()

    def __enter__(self):
        self.entered_context = True
        return self

    def __exit__(self, *exc):
        #for pid, agent in self.agents.items():
        #    self.loop.run_until_complete(agent.execute())
        tasks = [agent.execute() for agent in self.agents.values()]
        #asyncio.ensure_future(*tasks, loop=self.loop)
        self.loop.run_until_complete(asyncio.wait(tasks))

        self.loop.close()
        return False

class RootContext(ContextDecorator, AgentMixin):
    def __init__(self, loop, debug=False):
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.ERROR)

    def start(self, agent_fn, *args, **kwargs):
        pass

    def send():
        pass

    def recv():
        pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return false

def get_agent_context(loop=asyncio.get_event_loop(), debug=False):
    return RootContext(loop, debug=debug)
