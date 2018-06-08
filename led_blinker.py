import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import os
import RPi.GPIO as GPIO
import argparse
import signal
import sys
import time
import socket
import logging
import json
import subprocess

### GPIO
# ingore any warnings
GPIO.setwarnings(False)
# Declare variables
GPIO.setmode(GPIO.BCM)
# motor inputs
GPIO_STBY = 12
GPIO_PWMA = 13
GPIO_AIN2 = 5
GPIO_AIN1 = 6 
GPIO_ENDSTOP_TOP = 10
GPIO_ENDSTOP_BOTTOM = 22
motor_time = .1

# proportion for which the Motor is ON over the total time
dutycycle = 20
dutycycledown = 15
freq = 50

# LED
GPIO_GREEN   = 21
GPIO_RED     = 26
GPIO_LED_BLUE_UP = 17
GPIO_LED_BLUE_DOWN = 18
initial_GREEN = 1 #initial value in program for GREEN LED
# for red LED
numTimes = 4




# setup GPIO pins
GPIO.setup(GPIO_PWMA,GPIO.OUT)
GPIO.setup(GPIO_AIN2,GPIO.OUT)
GPIO.setup(GPIO_AIN1,GPIO.OUT)
GPIO.setup(GPIO_STBY,GPIO.OUT)
GPIO.setup(GPIO_ENDSTOP_TOP,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_ENDSTOP_BOTTOM,GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Set the PWM for pins
pwmA = GPIO.PWM(GPIO_PWMA, freq)

# Set Pins for the LEDS
GPIO.setup(GPIO_GREEN, GPIO.OUT)
GPIO.setup(GPIO_RED, GPIO.OUT)
  # LED blue for Glimmer
GPIO.setup(GPIO_LED_BLUE_UP, GPIO.OUT)# set GPIO 17 for blue LED
GPIO.setup(GPIO_LED_BLUE_DOWN, GPIO.OUT)# set GPIO 18 for blue LED

#set LED, motor standby, and motor PWM pins to be initially off
GPIO.output(GPIO_AIN2, False)
GPIO.output(GPIO_AIN1, False)
GPIO.output(GPIO_STBY, False)
GPIO.output(GPIO_PWMA, False)
GPIO.output(GPIO_GREEN, False)
GPIO.output(GPIO_RED, False)
GPIO.output(GPIO_LED_BLUE_UP, False)# set GPIO 17 for blue LED
GPIO.output(GPIO_LED_BLUE_DOWN, False)# set GPIO 18 for blue LED



### General


### MQTT
broker = '192.168.0.23'
topic ='legogarage/cover/set'
mqttQos = 0
mqttRetained = False


def post_garage_sensor_state(data):
    print('Posting Garage Door Status')
    client.publish('legogarage/cover/get', data, mqttQos, mqttRetained)  #

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    payload = str(msg.payload.decode('ascii'))  # decode the binary string
    print(msg.topic + " " + payload)
    process_trigger(payload)

def process_trigger(payload):
    if payload == 'OPEN':
        print('OPEN triggered')
        data = 'open' # lower case for the state of the sensor
        garage_command(payload)
        post_garage_sensor_state(data)

    if payload == 'CLOSE':
        print('CLOSE triggered')
        data = 'closed' # lower case for the state of the sensor
        garage_command(payload)
        post_garage_sensor_state(data)


def garage_command(payload): 
    i = 0
    if payload == 'OPEN':
        # Drive Motors Counter-clockwise
        GPIO.output(GPIO_AIN2, False)
        GPIO.output(GPIO_AIN1, True)
        endstop = GPIO.input(GPIO_ENDSTOP_TOP)
        pwmA.start(dutycycle)
        GPIO.output(GPIO_STBY, True)
        while (endstop):
            endstop = GPIO.input(GPIO_ENDSTOP_TOP)
            i += 1
    if payload == 'CLOSE':
        # Drive Motors Counter-clockwise
        GPIO.output(GPIO_AIN2, True)
        GPIO.output(GPIO_AIN1, False)
        GPIO.output(GPIO_STBY, True)
        pwmA.start(dutycycledown)
        endstop = GPIO.input(GPIO_ENDSTOP_BOTTOM)
        while (endstop):
            endstop = GPIO.input(GPIO_ENDSTOP_BOTTOM)
            i += 1
    # Reset all motors to shut off
    pwmA.stop()
    GPIO.output(GPIO_STBY,False)
    print("done")
    print(i)
    endstop = 0

print("starting to connect")
client = mqtt.Client()
client.username_pw_set(username='pi',password='peterbilt')  # need this

client.on_connect = on_connect    # call these on connect and on message
client.on_message = on_message

client.connect(broker)
print("connected")
client.loop_start()    #  run in background and free up main thread



# ### RF
# # pyli disabe=unused-argument
# def exitandler(signal, frame):
#     rfvice.cleanup()
#     sys.exit(0)

# logging.basiConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
#                     format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

try:
    while True:
        pass
finally:
    client.loop_stop()
    GPIO.cleanup()