from . import sync
from . import util
from asyncio import sleep
from asgiref.sync import sync_to_async


class Runner(sync.Runner):

    def __init__(self, language, version='default'):
        super().__init__(language, version, block=False)

    async def is_ready(self):
        while not self.container:
            await sleep(0.1)

setattr(Runner, "get_output", sync_to_async(sync.Runner.get_output))


