# Finn
from simspark_controller import simspark_controller


class CVAgent:
    def __init__(self):
        simspark_controller.foo()
        self.goal_center = (100, 100)  # Center of Goal in Pixels
        self.goal_size = (100, 200)  # width, height

    def update(self, perception) -> None:
        pass


cv_agent = CVAgent()
