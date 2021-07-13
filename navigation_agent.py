# Maksim
from cv_agent import cv_agent
from walking_agent import walking_agent


class NavigationAgent:
    def __init__(self):
        pass

    def update(self, perception):
        cv_agent.update(perception)
        x, y, z = self.__calc_walking_dir()
        walking_agent.walk_to(x, y, z)

    def __calc_walking_dir(self) -> tuple:
        goal_size = cv_agent.goal_size
        goal_center = cv_agent.goal_center
        # TODO calculation
        x = 1
        y = 2
        z = 3
        return x, y, z


navigation_agent = NavigationAgent()
