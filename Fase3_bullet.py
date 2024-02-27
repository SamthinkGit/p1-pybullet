from utils import entities
from utils.pybullet_consts import PBConsts
from utils.templates import Husky

import argparse
import pybullet as pb
import pybullet_data
import time

if __name__ == '__main__':

    # Partsing optional arguments
    parser = argparse.ArgumentParser(description='Runs a simulation of the husky driving through a barrier')
    parser.add_argument('--mode', type=float, help='Select a mode for running', choices=[3.1, 3.2, 3.3], default=3.3)
    parser.add_argument('--csv', type=str, help='Select the name for the output csv file.', default='Fase3.csv')
    args = parser.parse_args()

    # Starting GUI
    client = pb.connect(pb.GUI)
    pb.setAdditionalSearchPath(pybullet_data.getDataPath())
    pb.setGravity(*PBConsts.GRAVITY)

    # Entities
    plane = pb.loadURDF("plane.urdf")
    husky = pb.loadURDF("husky/husky.urdf")
    ramp = pb.loadURDF(entities.get_sample_path("ramp.urdf"))
    barrier = pb.loadURDF(entities.get_sample_path("barrier.urdf"), useFixedBase=True)
    goal = pb.loadURDF(entities.get_sample_path("goal.urdf"))

    entities.aling_to_ground(ramp, x=10)
    entities.aling_to_ground(barrier)
    entities.aling_to_ground(barrier, x=17, y=1.5, shift=-0.4)
    entities.aling_to_ground(goal, x=20)

    # Running Simulation
    pb.setRealTimeSimulation(1)

    # Wrapping Husky
    husky = Husky(husky)
    husky.set_velocity_to(vel=13, forces=25) 

    if args.mode >= 3.2:
        husky.set_dynamics(
            links=husky.wheels_idx,
            lateralFriction=0.93,
            spinningFriction=0.005,
            rollingFriction=0.003
        )

    if args.mode == 3.3:
        stick = entities.find_joint_idx('base2stick', barrier)
        pb.changeDynamics(barrier, stick, localInertiaDiagonal=[5.0, 5.0, 5.0])

    # Note: Velocity has been settled to 13 
    # so the husky doesn't get blocked

    try:
        while True:
            
            pos, _ = pb.getBasePositionAndOrientation(husky.info['id'])

            if pos[0] >= 20:
                break

            if pos[0] - husky.info['pos']['x'] < PBConsts.DISTANCE_FREQUENCY:
                time.sleep(PBConsts.CONTINOUS_FREQUENCY)
                continue

            husky.update()
            pass

    except KeyboardInterrupt as k:
        print("Interruption Received, Cleaning")

    husky.to_csv(name=f"csv_output/{args.csv}")
    print("Program Stopped. Closing GUI")
    pb.disconnect()