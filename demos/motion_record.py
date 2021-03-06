#!/usr/bin/env python3

import numpy as np #will use to create arrays
import pickle #will use to save data between program launches
import time

import sys
import argparse
import consts

from blue_interface import BlueInterface  # this is the API for the robot

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Record motion of a blue arm.')
    parser.add_argument('record_file', type=str, help='Saves a recorded motion to this file')
    parser.add_argument('--address', default=consts.default_address, type=str, help='Address of the host computer')
    parser.add_argument('--port', default=consts.default_port, type=int, help='Port that the ros web host was started on')
    parser.add_argument('--frequency', default=consts.default_frequency, type=int, help='Record at a custom frequency (Hz)')
    args = parser.parse_args()

    filename = args.record_file

    arm = consts.default_arm
    address = args.address
    port = args.port
    frequency = args.frequency # In Hertz

    #blue = BlueInterface("left","10.42.0.1")  # creates object of class KokoInterface at the IP in quotes with the name 'blue'
    blue = BlueInterface(arm, address, port) #creates object of class KokoInterface at the IP in quotes with the name 'blue'
    blue.disable_control() #this turns off any other control currently on the robot (leaves it in gravtiy comp mode)

    joint_angle_list = [] #Initialize the list to hold our joint positions
    pose_list = []
    gripper_list = []

    input("Press enter to start recording. To finish recording press <ctrl+c>.")

    try:
        last_time = 0.0
        while True:
            position = blue.get_joint_positions() #record the pose, this function returns a dictionary object
            joint_angle_list.append(position)
            pose = blue.get_cartesian_pose()
            pose_list.append(pose)
            gripper_pos = blue.get_gripper_position()
            gripper_list.append(gripper_pos)
            print("Position recorded!")
            #while time.time() - last_time < 1.0/frequency:
            #    pass
            sleep_time = 1.0/frequency - (time.time() - last_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
            last_time = time.time()
    except:
        print(joint_angle_list)

    if len(joint_angle_list)==0:
        print('You did not save any positions')
    else:
        pickle.dump((joint_angle_list, pose_list, gripper_list, frequency), open(filename, "wb")) #uses the pickle function to write a binary file
        print('Your position list has been saved in the directory')

    time.sleep(2)
    blue.shutdown()
