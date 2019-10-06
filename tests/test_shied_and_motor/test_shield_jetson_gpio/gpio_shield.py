#!/usr/bin/env python

# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
# EXAMPLE SETUP
# Connect a button to pin 18 and GND, a pull-up resistor connecting the button
# to 3V3 and an LED connected to pin 12. The application performs the same
# function as the button_led.py but performs a blocking wait for the button
# press event instead of continuously checking the value of the pin in order to
# reduce CPU usage.
'''
GPIO JETSON

import RPi.GPIO as GPIO
import time

# Pin Definitons:
motor_esquerda = 12  # Board pin 12


def main():
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BOARD pin-numbering scheme
    GPIO.setup(motor_esquerda, GPIO.OUT)  # LED pin set as output
    
    #configurar botao do manao

    # Initial state for LEDs:
    GPIO.output(motor_esquerda, GPIO.LOW)

    print("Starting demo now! Press CTRL+C to exit")
    try:
        while True:
            print("Waiting for button event")
            #codigo do manao

            # event received when button pressed
            print("Button Pressed!")
            GPIO.output(motor_esquerda, GPIO.HIGH)
            time.sleep(10)
            GPIO.output(motor_esquerda, GPIO.LOW)
    finally:
        GPIO.cleanup()  # cleanup all GPIOs

if __name__ == '__main__':
    main()
'''


import signal
from xbox360controller import Xbox360Controller
import time

import RPi.GPIO as GPIO # gpio rpi

LEFT_PIN_MOTOR_FORWARD = 12
RIGHT_PIN_MOTOR_FORWARD = 5
s
LEFT_PIN_MOTOR_BACKWARD = 13
RIGHT_PIN_MOTOR_BACKWARD = 6

forward_ports = [LEFT_PIN_MOTOR_FORWARD, RIGHT_PIN_MOTOR_FORWARD]
backward_ports = [RIGHT_PIN_MOTOR_BACKWARD, LEFT_PIN_MOTOR_BACKWARD]
all_motor_ports = forward_ports.extend(backward_ports)

def configure_gpIO():
    GPIO.setmode(GPIO.BOARD)
    for port in all_motor_ports:
        GPIO.setup(port, GPIO.OUT) 
        GPIO.output(port, GPIO.LOW) 

def walk_forward():
    for port in forward_ports:
        GPIO.output(port, GPIO.HIGH)   

def walk_backward():
    for port in backward_ports:
        GPIO.output(port, GPIO.HIGH) 


def stop():
    for port in all_motor_ports:
        GPIO.output(port, GPIO.LOW)   


def on_axis_moved(axis):
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
    
def on_trigger_pressed(axis):
    print('Trigger pressed: value: {0}'.format(axis.value))


def main():
    try:
        configure_gpIO()
    except Exception as e:
        print (e)

    try:
        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            # Button A events
            controller.button_a.when_pressed = walk_forward
            controller.button_a.when_released = stop
            
            controller.button_b.when_pressed = walk_backward
            controller.button_b.when_released = stop
            
 
            # Left and right axis move event
            
            #controller.axis_l.when_moved = on_axis_moved
            controller.axis_l.when_moved = on_axis_moved

            controller.trigger_r.when_moved = on_trigger_pressed
            
            signal.pause()
    except KeyboardInterrupt:
        pass

main()
