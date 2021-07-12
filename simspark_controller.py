# Maksim
# add PYTHONPATH
import os
import sys

from robolib.spark_agent.spark_agent import SparkAgent


class SimsparkController(SparkAgent):
    def __init__(self):
        super(SimsparkController, self).__init__()

    def think(self, perception):
        print(perception.see)
        return super(SimsparkController, self).think(perception)


simspark_controller = SimsparkController()

if '__main__' == __name__:
    agent = simspark_controller
    agent.run()
