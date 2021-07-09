# Maksim
# add PYTHONPATH
import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lecture_code'))

from spark_agent import SparkAgent


class SimsparkController(SparkAgent):
    #def __init__(self):
        #pass

    def think(self, perception):
        print(perception.see)
        return super(SimsparkController, self).think(perception)

    def foo(self):
        print("hi")


simspark_controller = SimsparkController()

if '__main__' == __name__:
    agent = simspark_controller
    agent.run()
