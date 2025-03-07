from pyniryo import *
import params

def init_position():
    #Init
    params.global_state["robot"] = NiryoRobot(params.robot_ip)
    robot = params.global_state["robot"]
    robot.update_tool()
    robot.calibrate_auto()
    robot.clear_collision_detected()

    
    params.global_state["a1"] = robot.get_pose_saved("A1")
    params.global_state["h8"] = robot.get_pose_saved("H8")
    params.global_state["dead_pieces"] = robot.get_pose_saved("dead_pieces")
    params.global_state["wait_robot"] = robot.get_pose_saved("wait_robot")
    params.global_state["promotQ"] = robot.get_pose_saved("promotQ")
    params.global_state["promotR"] = robot.get_pose_saved("promotR")
    params.global_state["promotB"] = robot.get_pose_saved("promotB")
    params.global_state["promotN"] = robot.get_pose_saved("promotN")

    params.global_state["square_height"] = abs(params.global_state["h8"].y - params.global_state["a1"].y) / 7
    params.global_state["square_width"] = abs(params.global_state["h8"].x - params.global_state["a1"].x) / 7
    robot.move(params.global_state["wait_robot"])

def play_robot_sound(sound):
    if params.SOUND_ON:
        robot =  params.global_state["robot"]
        robot.play_sound(sound, wait_end=False)
def pick_position(pos):
    robot =  params.global_state["robot"]
    robot.open_gripper()
    new_pose = PoseObject(pos.x, pos.y, pos.z + 0.1, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)
    new_pose = PoseObject(new_pose.x, new_pose.y, pos.z, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)
    robot.close_gripper(hold_torque_percentage=50)
    new_pose = PoseObject(pos.x, pos.y, pos.z + 0.1, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)

def place_position(pos):
    robot =  params.global_state["robot"]
    new_pose = PoseObject(pos.x, pos.y, pos.z + 0.1, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)
    new_pose = PoseObject(new_pose.x, new_pose.y, pos.z, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)
    robot.open_gripper(hold_torque_percentage=50)
    new_pose = PoseObject(pos.x, pos.y, pos.z + 0.1, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)

def pick_position_pawn(pos):
    robot =  params.global_state["robot"]
    robot.open_gripper()
    new_pose = PoseObject(pos.x, pos.y, pos.z + 0.1, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)
    new_pose = PoseObject(new_pose.x, new_pose.y, pos.z - 0.015, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)
    robot.close_gripper(hold_torque_percentage=50)
    new_pose = PoseObject(pos.x, pos.y, pos.z + 0.115, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)

def place_position_pawn(pos):
    robot =  params.global_state["robot"]
    new_pose = PoseObject(pos.x, pos.y, pos.z + 0.1, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)
    new_pose = PoseObject(new_pose.x, new_pose.y, pos.z - 0.015, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)
    robot.open_gripper(hold_torque_percentage=50)
    new_pose = PoseObject(pos.x, pos.y, pos.z + 0.115, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)

def pick_position_pawn_forward(pos):
    robot =  params.global_state["robot"]
    robot.open_gripper()
    new_pose = PoseObject(pos.x, pos.y, pos.z + 0.1, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)
    new_pose = PoseObject(new_pose.x, new_pose.y, pos.z - 0.015, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)
    robot.close_gripper(hold_torque_percentage=50)
    new_pose = PoseObject(pos.x, pos.y, pos.z , pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)

def place_position_pawn_forward(pos):
    robot =  params.global_state["robot"]
    new_pose = PoseObject(pos.x, pos.y, pos.z , pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)
    new_pose = PoseObject(new_pose.x, new_pose.y, pos.z -0.015, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)
    robot.open_gripper(hold_torque_percentage=50)
    new_pose = PoseObject(pos.x, pos.y, pos.z + 0.1, pos.roll, pos.pitch, pos.yaw)
    robot.move(new_pose)

def get_pose_from_square(square):
    a1=  params.global_state["a1"] if params.global_state["side"] == 1 else  params.global_state["h8"]
    square_width = params.global_state["square_width"]
    square_height = params.global_state["square_height"]
    col = ord(square[0]) - ord('a') 
    row = int(square[1]) - 1        
    x = a1.x + row * square_width if params.global_state["side"] == 1 else a1.x - row * square_width
    y = a1.y - col * square_height if params.global_state["side"] == 1 else a1.y + col * square_height
    return PoseObject(x, y, a1.z, a1.roll, a1.pitch, a1.yaw)
