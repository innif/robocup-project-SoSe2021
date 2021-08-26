# Sebastian
from robolib import NaoqiClientAgent

class WalkingAgent:
    def __init__(self, server_uri):
        self._agent = NaoqiClientAgent(server_uri=server_uri)

    def walk_to(self, x, y, theta=0.0, wait=True):
        self._agent.moveTo(x, y, theta, run_async=(not wait))
