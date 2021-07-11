# Sebastian
from robolib import ClientAgent
from robolib.keyframes import tai_chi_chuan


class WalkingAgent(ClientAgent):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def walkTo(self, x: float, y: float, z: float) -> None:
        raise NotImplementedError()

    def dance(self):
        self.execute_keyframes(tai_chi_chuan())