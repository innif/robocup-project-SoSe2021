import scipy.interpolate

from robolib.agents.pid import PIDAgent
from robolib.keyframes import hello, wipe_forehead


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])
        # MY CODE HERE
        self._start_time = None
        self._prev_time = 0

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE

        if not self._start_time:
            self._start_time = perception.time

        rel_time = perception.time - self._start_time

        is_done = keyframes != ([], [], [])

        for i, joint_name in enumerate(keyframes[0]):
            times = keyframes[1][i]
            keys = keyframes[2][i]

            x = []
            x.extend(times)
            y = [key[0] for key in keys]

            k = len(x) - 1 if len(x) <= 3 else 3

            if rel_time > times[-1]:
                continue

            is_done = False

            tck = scipy.interpolate.splrep(x=x, y=y, k=k)
            r = scipy.interpolate.splev([rel_time + 0.025], tck)

            target_joints[joint_name] = r[0]

        if is_done:
            self._start_time = None
            self.keyframes = ([], [], [])

        return target_joints


if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # wipe_forehead(None)  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
