from time import sleep

from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer

from lib.agents.inverse_kinematics import InverseKinematicsAgent


class ServerAgent(InverseKinematicsAgent):
    '''ServerAgent provides RPC service
    '''
    # YOUR CODE HERE
    def __init__(self, ip_address='localhost', port=8888):
        super().__init__()
        self.__server = SimpleXMLRPCServer(addr=(ip_address, port), allow_none=True)

        self.__server.register_introspection_functions()
        self.__server.register_function(self.get_angle)
        self.__server.register_function(self.set_angle)
        self.__server.register_function(self.get_posture)
        self.__server.register_function(self.execute_keyframes)
        self.__server.register_function(self.get_transform)
        self.__server.register_function(self.set_transform)

        Thread(target=self.__server.serve_forever).start()

    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        # YOUR CODE HERE
        return self.perception.joint[joint_name]

    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        # YOUR CODE HERE
        self.target_joints[joint_name] = angle

    def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        return self.posture

    def execute_keyframes(self, key_frames):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        # YOUR CODE HERE
        self.keyframes = key_frames
        while self.keyframes[0]:
            sleep(0.2)

    def get_transform(self, name):
        '''get transform with given name
        '''
        # YOUR CODE HERE
        return self.transforms[name]

    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        self.set_transforms(effector_name, transform)

if __name__ == '__main__':
    agent = ServerAgent()
    agent.run()
