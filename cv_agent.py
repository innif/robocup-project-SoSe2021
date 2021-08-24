# Finn
from robolib import NaoqiClientAgent


class CVAgent:
    def __init__(self, server_uri):
        self._agent = NaoqiClientAgent(server_uri)
        self.goal_center = (100, 100)  # Center of Goal in Pixels
        self.goal_size = (100, 200)  # width, height

        self._agent.subscribe_to_cam(2, 11)

    def update(self, perception) -> None:
        pass

    def get_image(self):
        return self._agent.get_image()
