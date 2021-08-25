# Maksim
from cv_agent import CVAgent
from walking_agent import WalkingAgent

TARGET_COLOR = "yellow"

class NavigationAgent:
    def __init__(self, server_uri):
        self.__cv_agent = CVAgent(server_uri=server_uri)
        self.__walking_agent = WalkingAgent(server_uri=server_uri)
    
    def run(self):
        turn_to_goal()
        walk_to_goal()
     
    def update(self, target):
        self.__cv_agent.update(target)

    def turn_to_goal(self):
        """
        Turns the robot towards the goal until center of the goal is approximately in center of the robot's camera image.
        Please note: The robot's movement axis are not equal to the image's axis. Instead of just the head, the whole
        robot has to turn so the movement direction is correct afterwars.
        Image axis are like this:
         
         ^ y-Axis
         |
         |
         |
         |
         |-----------> x-Axis
        In order to "move" the goal on the x-axis of the camera image, the robot has to turn around its z-axis using the theta angle.
        The robot axis definitions can be found at http://doc.aldebaran.com/1-14/naoqi/motion/index.html#axis-definition
        """
        self.update(TARGET_COLOR)
        goal_center = self.__cv_agent.goal_center
        while goal_center[0] == None:
            self.__walking_agent.walk_to(0, 0, theta=0.1, wait=True)
            goal_center = self.__cv_agent.goal_center
        while(not -10 <= goal_center[0] <= 10):
            if(goal_center < 0):
                self.__walking_agent.walk_to(0, 0, theta=0.1, wait=True)
            else:
                self.__walking_agent.walk_to(0, 0, theta=-0.1, wait=True)
            self.update(TARGET_COLOR)
            goal_center = self.__cv_agent.goal_center
            
    def walk_to_goal(self):
        """
        Robot walks towards the goal as long as the goal size is below a certain threshold.
        Please note: The robot's x-movement axis is not equal to the image's x-axis
        """
        goal_size_threshold = (100, 50)
        self.update(TARGET_COLOR)
        goal_size = self.__cv_agent.goal_size
        if(goal_size == None):
            return
        while goal_size < goal_size_threshold:
            self.__walking_agent.walk_to(1, 0, theta=0, wait=True)
            self.update(TARGET_COLOR)
            goal_size = self.__cv_agent.goal_size



navigation_agent = NavigationAgent()
