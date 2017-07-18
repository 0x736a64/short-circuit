#!env/bin/python

# VERSION: 0.0.1
# DESCRIPTION: A Home Automation/Sensor API for RPi
# AUTHOR: 0x736a64
# CODENAME: Short Circuit

"""
ShortCircuit::SpyCam - motion triggered camera on Raspberry Pi

"""

import time
import datetime
import subprocess
try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print "Error importing RPi.GPIO library! Try running with as root."

class SpyCam(object):
    """
        SpyCam Class.
    """
    def __init__(self):
        self._pins = {
            'pir': 21 #Configurable to any GPIO pin
        }
        self._states = {
            'pir': True #congiruable boolean for usage of PIR
        }
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.get_pin('pir'), GPIO.IN)
        self.activate_pir()

    def get_pin(self, key):
        """
            Return a pin for a given key.
        """

        return self._pins[key]

    def get_state(self, key):
        """
            Return the current state of a value for a given key.
        """

        return self._states[key]

    def set_state(self, key, val):
        """
            Set the current state of a value for a given key.
        """

        self._states[key] = val

    def activate_pir(self):
        """
        Runs a loop to check if the PIR state has changed. If it has, a photo is taken.

        """

        if self.get_state('pir') == True:
            while True:
                if GPIO.input(self.get_pin('pir')):
                    self.take_still()
            time.sleep(1)
        return None

    def take_still(self):
        """
            Take a still photo using the Raspberry Pi Camera Module.

        """

        timestamp = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        outfile = 'Image' + timestamp + '.jpg'
        subprocess.call(['raspistill', '-o', outfile])
        return 'Image Captured!'


if __name__ == '__main__':
    CAM = SpyCam()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CAM.get_pin('pir'), GPIO.IN)
    input('Press ENTER to exit')
