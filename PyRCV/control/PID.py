def damped_factor(x,max_factor,smoothing): 
    """This function makes the PID proportional factor smaller near the initial position (50% of RoM)
    It's used to dampen the rotation when the camera is near to looking directly to the target"""
    return ((smoothing)*x**2 + (1-smoothing))*max_factor

def correctCamera(object_center,frame):
    # Correct relative to centre of image
    turn_x  = float(object_center[0] - (frame[0]/2))
    turn_y  = float(object_center[1] - (frame[1]/2))

    # Convert to percentage offset
    turn_x  /= float(frame[0]/2)
    turn_y  /= float(frame[1]/2)
    k_x = damped_factor(turn_x,15,.75)
    k_y = damped_factor(turn_x,15,.75)
        
    # Scale offset to degrees (that k_x value below acts like the Proportional factor in PID)
    turn_x   *= k_x # VFOV
    turn_y   *= k_y # HFOV
    cam_pan   = -turn_x
    cam_tilt  = turn_y
    ANG = [cam_pan,cam_tilt]
    return ANG