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
