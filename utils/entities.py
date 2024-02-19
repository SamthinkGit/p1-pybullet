import pybullet as pb
from pathlib import Path

def aling_to_ground(object_id: int, x: float = 0.0, y: float = 0.0, orientation: list = [0,0,0,1]) -> None:
    """
    Sets the position of an entitie aligned to ground
    Assumes ground is the plane 0,0
    Args:
        param x: x location
        param y: y location
        param orientation: Orientation of the entity in quaternion
    """
    aabb = pb.getAABB(object_id)
    pb.resetBasePositionAndOrientation(object_id, [x, y, aabb[1][2]], orientation)
    return None

def find_joint_idx(joint_name: str, object_id: int) -> int:
    """
    Finds the identifier of a joint in an entity
    Args:
        joint_name: name of the joint to be searched in the entity
        object_id: Id of the entity
    """

    joint_idx = None

    for i in range(pb.getNumJoints(object_id)):

        joint_info = pb.getJointInfo(object_id, i)
        if joint_info[1].decode('utf-8') == joint_name:
            joint_idx = i
            break

    assert joint_idx is not None, f"Joint {joint_name} not found in entity "
    return joint_idx


def get_sample_path(name: str) -> str:
    root_dir = Path(__file__).resolve().parent.parent
    return str(root_dir / "samples" / name)

    

