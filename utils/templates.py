import pybullet as pb
import utils.entities as entities
import csv

class Husky():
    
    wheel_names = ['front_left_wheel', 'front_right_wheel', 'rear_left_wheel', 'rear_right_wheel']
    TO_CSV_SEPARATOR = '_'

    def __init__(self, id: int) -> None:


        wheels_idx = [entities.find_joint_idx(name, id) for name in Husky.wheel_names]

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
                name: { 'idx': idx, 'torque': 0, 'vel': 0 } for name, idx in zip(Husky.wheel_names, wheels_idx)
            },
        }
        self.history: list[dict] = []
        
    def update(self):

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

        self.history.append(Husky._linearize_register(self.info))


    def to_csv(self, name: str = 'husky_info.csv'):

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

