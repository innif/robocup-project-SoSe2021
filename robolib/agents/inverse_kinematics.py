from robolib.agents.forward_kinematics import ForwardKinematicsAgent
from math import atan2
from numpy import asarray, linalg, matrix
from numpy.matlib import identity
from scipy.linalg import pinv


class InverseKinematicsAgent(ForwardKinematicsAgent):
    def inverse_kinematics(self, effector_name, transform):
        '''solve the inverse kinematics

        :param str effector_name: name of end effector, e.g. LLeg, RLeg
        :param transform: 4x4 transform matrix
        :return: list of joint angles
        '''
        joint_angles = []
        # YOUR CODE HERE

        # jacobian implementation from ./inverse_kinematics_2d_jacobian.ipynb
        def from_trans(m):
            '''get x, y, theta from transform matrix'''
            return [m[0, -1], m[1, -1], atan2(m[1, 0], m[0, 0])]

        lambda_ = 1
        max_step = 0.1

        current_joints = {}
        for joint in self.chains[effector_name]:
            current_joints[joint] = self.perception.joint[joint]

        target = from_trans(transform)

        for i in range(1000):
            self.forward_kinematics(current_joints)
            Ts = list(self.transforms.values())
            Te = matrix([from_trans(Ts[-1])]).T
            e = target - Te
            e[e > max_step] = max_step
            e[e < -max_step] = -max_step
            T = matrix([from_trans(i) for i in Ts[1:-1]]).T
            J = Te - T
            dT = Te - T
            J[0, :] = -dT[1, :]  # x
            J[1, :] = dT[0, :]  # y
            J[-1, :] = 1  # angular
            d_theta = lambda_ * pinv(J) * e
            for i, joint in enumerate(self.chains[effector_name]):
                current_joints[joint] += asarray(d_theta.T)[0][i]

            if linalg.norm(d_theta) < 1e-4:
                break

        joint_angles = list(current_joints.values())
        return joint_angles


    def set_transforms(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        calculated_joint_angles = self.inverse_kinematics(effector_name, transform)
        names = self.chains[effector_name]
        times = [[1.0 , 3.0]] * len(names)
        keys = [
            list((
                [self.perception.joint[name], [3, 0, 0], [3, 0, 0]],
                [calculated_joint_angles[i], [3, 0, 0], [3, 0, 0]]
            ))
            for i, name in enumerate(names)
        ]

        self.keyframes = (names, times, keys)  # the result joint angles have to fill in


if __name__ == '__main__':
    agent = InverseKinematicsAgent()
    # test inverse kinematics
    T = identity(4)
    T[-1, 1] = 0.05
    T[-1, 2] = 0.26
    agent.set_transforms('LLeg', T)
    agent.run()
