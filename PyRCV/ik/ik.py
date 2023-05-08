import ikpy.chain
import ikpy.utils.plot as plot_utils

import numpy as np
import time
import math

######INPUTS##########

extended_length = 0.45 
target_pos = [0.3, 0.3,0.1]
target_or = [0, 0, 0]

######################

def move(path,target_position,target_orientation,extended_length):
    my_chain = ikpy.chain.Chain.from_urdf_file("/home/oscar/Desktop/arm_urdf.urdf",active_links_mask= \
                                           [False, True, True, True, True, True])
    global ik
    old_position= ik.copy()
    
    total_length = (target_position[0]**2+target_position[1]**2+target_position[2]**2)**0.5
    ik = my_chain.inverse_kinematics(target_position, target_orientation, orientation_mode="Z", initial_position=old_position)
    angles = list(map(lambda r:math.degrees(r),ik.tolist()))
