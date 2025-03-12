from pyniryo import * 

robot_ip = "192.168.0.102"
robot = NiryoRobot(robot_ip)
robot.update_tool()
robot.calibrate_auto()

end_pos = robot.get_pose()
nom_pos = "A1"
robot.save_pose(nom_pos,end_pos)
print(nom_pos," saved :",end_pos)

robot.close_connection()