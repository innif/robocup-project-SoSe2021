from threading import Thread
import weakref

from xmlrpc.client import ServerProxy

from robolib.keyframes import hello

class PostHandler(object):
    '''the post hander wraps function to be excuted in paralle
    '''
    def __init__(self, obj):
        self.proxy = weakref.proxy(obj)

    def execute_keyframes(self, key_frames):
        '''non-blocking call of ClientAgent.execute_keyframes'''
        # YOUR CODE HERE
        thread = Thread(target=self.proxy.execute_keyframes,
                        args=[key_frames])
        thread.start()
        return thread

    def set_transform(self, effector_name, transform):
        '''non-blocking call of ClientAgent.set_transform'''
        # YOUR CODE HERE
        thread = Thread(target=self.proxy.set_transform,
                        args=[effector_name, transform])
        thread.start()
        return thread


class ClientAgent(object):
    '''ClientAgent request RPC service from remote server
    '''
    # YOUR CODE HERE
    def __init__(self, server_uri='http://localhost:8888'):
        self._server_proxy = ServerProxy(server_uri, allow_none=True)
        self.post = PostHandler(self._server_proxy)

    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        # YOUR CODE HERE
        return self._server_proxy.get_angle(joint_name)

    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        # YOUR CODE HERE
        return self._server_proxy.set_angle(joint_name, angle)

    def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        return self._server_proxy.get_posture()

    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        # YOUR CODE HERE
        self.post.execute_keyframes(keyframes).join()

    def get_transform(self, name):
        '''get transform with given name
        '''
        # YOUR CODE HERE
        return self._server_proxy.get_transform(name)

    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        return self.post.set_transform(effector_name, transform)

if __name__ == '__main__':
    agent = ClientAgent()
    # TEST CODE HERE
    print(agent.get_angle('HeadYaw'))

    agent.execute_keyframes(hello())
    print('Done')
