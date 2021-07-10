import os
import pickle
import numpy as np
from sklearn import svm

from lib.agents.angle_interpolation import AngleInterpolationAgent
from lib.keyframes import hello


class PostureRecognitionAgent(AngleInterpolationAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(PostureRecognitionAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.posture = 'unknown'
        file_dir = os.path.dirname(__file__)
        with open(os.path.join(file_dir, 'robot_pose.pkl'), 'rb') as pickled_model:
            self.posture_classifier = pickle.load(pickled_model)  # LOAD YOUR CLASSIFIER
        self.possible_postures = os.listdir(os.path.join(file_dir, 'robot_pose_data'))

    def think(self, perception):
        self.posture = self.recognize_posture(perception)
        return super(PostureRecognitionAgent, self).think(perception)

    def recognize_posture(self, perception):
        posture = 'unknown'
        # YOUR CODE HERE
        data = []

        for feature in ['LHipYawPitch', 'LHipRoll', 'LHipPitch',
                        'LKneePitch', 'RHipYawPitch', 'RHipRoll',
                        'RHipPitch', 'RKneePitch']:
            data.append(perception.joint[feature])

        data.extend(perception.imu)

        posture_index = self.posture_classifier.predict([data])

        posture = self.possible_postures[int(posture_index)]

        return posture

if __name__ == '__main__':
    agent = PostureRecognitionAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
