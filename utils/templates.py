import pybullet as pb
import utils.entities as entities
from utils.pybullet_consts import CALIBRATION
import csv

from utils.control import PID
from icecream import ic
from typing import Union


class Husky():
    
    wheel_names = ['front_left_wheel', 'front_right_wheel', 'rear_left_wheel', 'rear_right_wheel']

    TO_CSV_SEPARATOR = '_'


    def __init__(self, id: int) -> None:

        self.wheels_idx = [entities.find_joint_idx(name, id) for name in Husky.wheel_names]
        self.pid = None
        self.forces = None
        self.input_vel = None
        self.info = {
            'id': id,
            'frame': 0,
            'time': 0,
            'vel': {
                'x': 0.0,
                'y': 0.0,
                'z': 0.0
            },
            'pos': {
                'x': 0.0,
                'y': 0.0,
                'z': 0.0
            },
            'wheels': {
                name: { 'idx': idx, 'torque': 0, 'vel': 0 } for name, idx in zip(Husky.wheel_names, self.wheels_idx)
            },
        }
        self.history: list[dict] = []
        
    def set_pid(self, pid: PID, umbral: float = float('inf')):

        self.pid = pid
        self.umbral = umbral
        self.info['Kp'] = pid.Kp
        self.info['Ki'] = pid.Ki
        self.info['Kd'] = pid.Kd
        self.info['umbral'] = self.umbral
        self.info['err'] = pid.previous_error

    def update(self) -> None:

        self.info['frame'] += 1
        self.info['time'] += pb.getPhysicsEngineParameters()['fixedTimeStep']
        
        pos, _ = pb.getBasePositionAndOrientation(self.info['id'])
        self.info['pos']['x'] = pos[0]
        self.info['pos']['y'] = pos[1]
        self.info['pos']['z'] = pos[2]

        vel, _ = pb.getBaseVelocity(self.info['id'])
        self.info['vel']['x'] = vel[0]
        self.info['vel']['y'] = vel[1]
        self.info['vel']['z'] = vel[2]
        
        for wheel in self.info['wheels'].values():
            joint_state = pb.getJointState(self.info['id'], wheel['idx'])
            wheel['vel'] = joint_state[1]
            wheel['torque'] = joint_state[3]

        if self.pid is not None:
            self.info['err'] = self.pid.previous_error
            self.info['pid_out'] = self.pid.prev_output

    def save(self):
        self.history.append(Husky._linearize_register(self.info))
    
    def auto_adjust(self):

        assert self.forces is not None, "[Husky] Trying to auto-adjust husky without having settled forces"

        adjust = self.pid.update(self.info['vel']['x'])
        # [5 -> 15] (12)
        # *2 
        # [10 -> 30]
        # Fuerzas: POR DEFECTO 25
        self.set_velocity_to(vel=adjust, forces=CALIBRATION.FORCE_SHIFT) 

    def set_velocity_to(
            self, 
            vel: Union[int, float, list[float]], 
            forces: Union[int, float, list[float]]
        ) -> None:

        if isinstance(vel, (int, float)):
            vel = [vel]*len(self.wheels_idx)

        if isinstance(forces, (int, float)):
            forces = [forces]*len(self.wheels_idx)

        self.input_vel = vel
        self.forces = forces

        pb.setJointMotorControlArray(
            bodyIndex=self.info['id'],
            jointIndices=self.wheels_idx,
            controlMode=pb.VELOCITY_CONTROL,
            targetVelocities=vel,
            forces=forces,
        )
    
    def set_dynamics(self, links: list[str], **kwargs):

        for link in links:
            pb.changeDynamics(
                bodyUniqueId=self.info['id'],
                linkIndex=link,
                **kwargs
            )


    def to_csv(self, name: str = 'husky_info.csv') -> None:

        with open(name, 'w', newline='') as f:
            writer = csv.DictWriter(f, self.history[0].keys())
            writer.writeheader()
            for entry in self.history:
                writer.writerow(entry)

    def _linearize_register(register: dict, parent_key='', sep='_') -> dict:
        # Thanks to @OphirCarmi for his implementation at:
        # https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys

        items = []

        for key, val in register.items():

            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(val, dict):
                items.extend(Husky._linearize_register(val, new_key, sep=sep).items())
            
            else:
                items.append((new_key, val))

        return dict(items)

