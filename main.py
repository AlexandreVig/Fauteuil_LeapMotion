################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

from turtle import forward
import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from pyduino import *


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

    def on_init(self, controller):
        # if your arduino was running on a serial port other than '/dev/ttyACM0/'
        # declare: a = Arduino(serial_port='/dev/ttyXXXX')
        self.a = Arduino()
        
        # sleep to ensure ample time for computer to make serial connection 
        time.sleep(3)
        
        # Define Pins for Arduino Motor
        self.Moteur_G = 6 # Left Motor
        self.Moteur_D = 5 # Right Motor 
        self.Buzzer = 9 # Buzzer

        # allow time to make connection
        time.sleep(1)

        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        time.sleep(1)
        # Shuting down everything
        self.a.send_command(self.Moteur_G, 0, forward=True) # Shutdown Left Motor
        self.a.send_command(self.Moteur_D, 0, forward=True) # Shutdown Right Motor
        self.a.close() # Close Serial Connection

        print "Exited"

    def on_frame(self, controller):
        time.sleep(1)
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
                frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))
        
        if len(frame.hands) == 0:
            self.a.send_command(self.Moteur_G, 0, forward=True) # Shutdown Left Motor
            self.a.send_command(self.Moteur_D, 0, forward=True) # Shutdown Right Motor

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Get the pith angle to go forward or backward
            pitch = direction.pitch * Leap.RAD_TO_DEG

            # Get roll angle to go left or right
            roll = normal.roll * Leap.RAD_TO_DEG

            # Get speed of motor
            speed_pitch = map_range(-90, -15, 100, 255, pitch)

            # Get speed of motor
            speed_roll = map_range(-180, 180, -255, 255, roll)

            # Turn the motors
            if pitch < -20:
                self.a.send_command(self.Moteur_G, speed_pitch, forward=True)
            else:
                if roll > 0:
                    self.a.send_command(self.Moteur_D, 255, turn="Left")
                elif roll < 0:
                    self.a.send_command(self.Moteur_G, 255, turn="Right")


            # Calculate the hand's pitch, roll, and yaw angles
            print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            '''arm = hand.arm
            print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
                arm.direction,
                arm.wrist_position,
                arm.elbow_position)'''

    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def map_range(min_orig, max_orig, min_new, max_new, value):
    """ Map a value from a range to another range.

    Args:
        min_orig (int): The original minimum value.
        max_orig (int): The original maximum value.
        min_new (int): The new minimum value.
        max_new (int): The new maximum value.
        value (int): The value to map.
    
    Returns:
        int: The mapped value.
    """
    if value < min_orig:
        return min_new
    if value > max_orig:
        return max_new
    else:
        range_orig = max_orig - min_orig
        range_new = max_new - min_new
        ratio = range_new / range_orig
        return (value - min_orig) * ratio + min_new # new value

def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
