import signal
from xbox360controller import Xbox360Controller
import time

def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))

def on_button_released(button):
    print('Button {0} was released'.format(button.name))

def on_axis_moved(axis):
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
    
def on_trigger_pressed(axis):
    print('Trigger pressed: value: {0}'.format(axis.value))

try:
    with Xbox360Controller(0, axis_threshold=0.2) as controller:
        # Button A events
        controller.button_a.when_pressed = on_button_pressed
        #controller.button_a.when_released = on_button_released

        # Left and right axis move event
        
        #controller.axis_l.when_moved = on_axis_moved
        controller.axis_l.when_moved = on_axis_moved

        controller.trigger_r.when_moved = on_trigger_pressed
        
        signal.pause()
except KeyboardInterrupt:
    pass
