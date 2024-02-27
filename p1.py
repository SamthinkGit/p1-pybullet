from icecream import ic
from utils import entities
from utils.pybullet_consts import PBConsts
from utils.templates import Husky

import pybullet as pb
import pybullet_data
import time

if __name__ == '__main__':

    # Starting GUI
    client = pb.connect(pb.GUI)
    pb.setAdditionalSearchPath(pybullet_data.getDataPath())
    pb.setGravity(*PBConsts.GRAVITY)

    # Entities
    plane = pb.loadURDF("plane.urdf")
    husky = pb.loadURDF("husky/husky.urdf")
    ramp = pb.loadURDF(entities.get_sample_path("ramp.urdf"))
    barrier = pb.loadURDF(entities.get_sample_path("barrier.urdf"))
    goal = pb.loadURDF(entities.get_sample_path("goal.urdf"))

    entities.aling_to_ground(ramp, x=10)
    entities.aling_to_ground(barrier)
    entities.aling_to_ground(barrier, x=17, y=1.5)
    entities.aling_to_ground(goal, x=20)

    # Obtaining Joints
    wheel_names = ['front_left_wheel', 'front_right_wheel', 'rear_left_wheel', 'rear_right_wheel']
    wheels_idx = [entities.find_joint_idx(name, husky) for name in wheel_names]
    
    # Running Simulation
    pb.setRealTimeSimulation(1)

    # Settling Velocity
    pb.setJointMotorControlArray(
        bodyIndex=husky,
        jointIndices=wheels_idx,
        targetVelocities=[10 for _ in wheels_idx],
        controlMode=pb.VELOCITY_CONTROL
    )

    # Wrapping Husky
    husky = Husky(husky)

    try:
        while True:

            pos, _ = pb.getBasePositionAndOrientation(husky.info['id'])

            if pos[0] - husky.info['pos']['x'] < PBConsts.DISTANCE_FREQUENCY:
                time.sleep(PBConsts.CONTINOUS_FREQUENCY)
                continue

            husky.update()
            pass

    except KeyboardInterrupt as k:

        husky.to_csv()
        print("Program Stopped. Closing GUI")
        pb.disconnect()