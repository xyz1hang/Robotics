# Jaikrishna Initial Date: June 24, 2013 Last Updated: June 24, 2013
#
# These files have been made available online through a Creative Commons Attribution-S$
# (http://creativecommons.org/licenses/by-sa/3.0/)
#
# http://www.dexterindustries.com/
# This code is for testing the BrickPi with a Lego Motor 

from BrickPi import *   #import BrickPi.py file to use BrickPi operations
import numpy
from numpy import *
import math
LEFT_MOTOR = PORT_A
RIGHT_MOTOR = PORT_C
LEFT_TOUCHSENSOR = PORT_3
RIGHT_TOUCHSENSOR = PORT_1
SONAR_SENSOR = PORT_2
AVE_SPEED = 180
current_x = 0
current_y = 0
current_theta = 0.0

def bumper_left_hit():
    return BrickPi.Sensor[LEFT_TOUCHSENSOR]

def bumper_right_hit():
    return BrickPi.Sensor[RIGHT_TOUCHSENSOR]
    
def get_distance():
    return BrickPi.Sensor[SONAR_SENSOR]
    
def get_speed():
    return "[" + str(BrickPi.MotorSpeed[LEFT_MOTOR]) + ", " + str(BrickPi.MotorSpeed[RIGHT_MOTOR]) + "]"

def direction():
    return BrickPi.MotorSpeed[LEFT_MOTOR] - BrickPi.MotorSpeed[RIGHT_MOTOR] + 5

def move_forward():
    BrickPi.MotorEnable[LEFT_MOTOR] = 1 #Enable the Motor A
    BrickPi.MotorEnable[RIGHT_MOTOR] = 1 #Enable the Motor B
    BrickPi.MotorSpeed[LEFT_MOTOR] = 85  #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[RIGHT_MOTOR] = 90  #Set the speed of MotorB (-255 to 255)
    
def updatable_move(leftSpeed, rightSpeed):
    if not leftSpeed == None:
        BrickPi.MotorSpeed[LEFT_MOTOR] = leftSpeed
    if not rightSpeed == None:
        BrickPi.MotorSpeed[RIGHT_MOTOR] = rightSpeed
    
def change_speed(Speed):
    BrickPi.MotorSpeed[LEFT_MOTOR] = Speed + 5 #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[RIGHT_MOTOR] = Speed  #Set the speed of MotorB (-255 to 255)

def stop():
    BrickPi.MotorSpeed[LEFT_MOTOR] = 0 # stop the motor
    BrickPi.MotorSpeed[RIGHT_MOTOR] = 0 # stop the motor

def forward_40cm():
    motorRotateDegree([105,100],[750,750],[LEFT_MOTOR,RIGHT_MOTOR]) #Set the circle bo$
#    BrickPi.MotorSpeed[PORT_A] = 180  #Set the speed of MotorA (-255 to 255)
#    BrickPi.MotorSpeed[PORT_B] = 173  #Set the speed of MotorB (-255 to 255)
#    ot = time.time()
#    while(time.time() - ot < 1.26):    #running while loop for 3 seconds
#        BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
#        time.sleep(.1)                   # sleep for 500 ms
#    time.sleep(1.5)

def left_90deg():

    motorRotateDegree([103,103],[-125,125],[LEFT_MOTOR,RIGHT_MOTOR])
#    BrickPi.MotorSpeed[PORT_A] = -83  #Set the speed of MotorA (-255 to 255)
#    BrickPi.MotorSpeed[PORT_B] = 83  #Set the speed of MotorB (-255 to 255)
#    ot = time.time()
#    while(time.time() - ot < 0.875):    #running while loop for 1 seconds
#        BrickPiUpdateValues()       # Ask BrickPi to update values for sensors/motors
#        time.sleep(.1)             # sleep for 500 ms
#    time.sleep(1.5)

def right_90deg():
    motorRotateDegree([103,103],[125,-125],[LEFT_MOTOR,RIGHT_MOTOR])

def reverse():
    motorRotateDegree([103,103],[-225,-225],[LEFT_MOTOR,RIGHT_MOTOR])

def run_oneRound():
    forward_40cm()
    left_90deg()
    forward_40cm()
    left_90deg()
    forward_40cm()
    left_90deg()
    forward_40cm()
    left_90deg()

def run_touchSensor():
    hit = False
    move_forward()
    while not hit:
        result = BrickPiUpdateValues()          # Ask BrickPi to update values for motors$
        if not result:
            if (bumper_left_hit() or bumper_right_hit()):
                hit = True
        time.sleep(.1)

        if hit:
            stop()        # stop the motor
            if not (bumper_left_hit() and bumper_right_hit()) :
                if (bumper_left_hit()):
                    reverse()
                    right_90deg()
                elif (bumper_right_hit()):
                    reverse()
                    left_90deg()
            else :
                reverse()
                left_90deg()
            hit = False
            move_forward()

def init_sonarSensor():
    distances = zeros(5,int)
    #print distances
    for i in range(5):
        BrickPiUpdateValues()
        distances[i] = get_distance()
        time.sleep(.02)
    return distances

def run_sonarSensor():
    count = 0
    distances = init_sonarSensor()
    move_forward()
    while True:
        BrickPiUpdateValues()
        if count < 4:
            distances[count] = get_distance()
            count += 1
        elif count == 4:
            count = 0
            distances[count] = get_distance()
            count += 1
        distance = median(distances)
        distance = median(init_sonarSensor())
        print distance
        if distance > 30:
            change_speed(int(110*(distance-30)/70)+70)
        print "forward"
        elif distance < 30:
            change_speed(int(-110*(30-distance)/70)-70)
        print "reverse"
        else: 
            change_speed(0)
        print get_speed()
        #time.sleep(.1)


def run_walkalongwall():
    move_forward()
    after_dis = median(init_sonarSensor())
    count = 0
    while not (bumper_left_hit() or bumper_right_hit()):
        BrickPiUpdateValues()
        pre_dis = after_dis
        after_dis = median(init_sonarSensor())
        diff_dis = after_dis - pre_dis
        #distance = median(distances)
        #if after_dis > 30 and diff_dis > 0:
        if direction() > 2:            #if it is turing right
            if after_dis > 30:         #if the distance is greater than 30
                if diff_dis > 0:               #if distance is increasing (turing right too much)
                    rightspeed = int(90 + (after_dis - 30)*1.5)
                    updatable_move(85,rightspeed)
                else:
                    pass
            if after_dis < 30:
                # begin to turn left
                rightspeed = int(90 + (30 - after_dis)*1.5)
                updatable_move(85,rightspeed)
        elif direction() < -2:           #if it is turing left
            if after_dis > 30:       #if the distance is greater than 30
                leftspeed = int(85 + (after_dis - 30)*1.5)
                updatable_move(leftspeed, 90)
            elif after_dis < 30:
                if diff_dis < 0:
                    rightspeed = int(90 + (30 - after_dis)*2)
                    updatable_move(85,rightspeed)
                pass
        else:
            if after_dis > 30:       #if the distance is greater than 30
                # begin to turn right
                leftspeed = int(85 + (after_dis - 30)*1.5)
                updatable_move(leftspeed, 90)
            elif after_dis < 30:
                # begin to turn left
                rightspeed = int(90 + (30 - after_dis)*1.5)
                updatable_move(85,rightspeed)

        print after_dis
        print get_speed()

def forward(distance):
    global current_x,current_y,current_theta
    motorRotateDegree([160,160],[18.75*distance,18.75*distance],[LEFT_MOTOR,RIGHT_MOTOR])
    current_x = current_x + distance*math.cos(current_theta*math.pi/180)
    current_y = current_y + distance*math.sin(current_theta*math.pi/180)

def turn(degrees):
    global current_x,current_y,current_theta
    motorRotateDegree([123,123],[-1.950*degrees,1.950*degrees],[LEFT_MOTOR,RIGHT_MOTOR])
    current_theta = current_theta + degrees
    if current_theta > 180:
        current_theta -= 360
    elif current_theta <-180:
        current_theta += 360

def navigateToWaypoint(x,y):
    print [x,y]
    global current_x,current_y,current_theta
    print [current_x,current_y]
    distance = pow(pow(x-current_x,2)+pow(y-current_y,2),0.5)
    print x == current_x
    dif_y = float(round(y,3)-round(current_y,3))
    dif_x = float(round(x,3)-round(current_x,3))
    if dif_x == 0:
        if y > current_y:
            degrees = 90 - current_theta
            print "positive y"
        elif y < current_y:
            degrees = -90 - current_theta
            print "negative y"
    else:
        degrees = math.atan(dif_y/dif_x)/math.pi*180
        if dif_y > 0 and dif_x >0:
            degrees = degrees - current_theta
        elif dif_y > 0 and dif_x< 0:
            degrees = degrees - current_theta + 180
        elif dif_y <0  and dif_x > 0:
            degrees = degrees - current_theta
        elif dif_y < 0 and dif_x < 0:
            degrees = degrees -current_theta-180
        if degrees > 180:
            degrees -= 360
        elif degrees < -180:
            degrees += 360 
    print "current location: " + str(current_x)+"   "+str(current_y)
    print "current direction: " + str(current_theta)
    print "turn" + str(degrees)
    turn(degrees)
    time.sleep(1)
    print "forward" + str(distance)
    forward(distance)
    print "current location: " + str(current_x)+"   "+str(current_y)
    print "current direction: " + str(current_theta)

# Main 
# set up sensors
BrickPiSetup()  # setup the serial port for communication

BrickPi.MotorEnable[LEFT_MOTOR] = 1 #Enable the Motor A
BrickPi.MotorEnable[RIGHT_MOTOR] = 1 #Enable the Motor B

BrickPi.SensorType[LEFT_TOUCHSENSOR] = TYPE_SENSOR_TOUCH   #Set the type of sensor
BrickPi.SensorType[RIGHT_TOUCHSENSOR] = TYPE_SENSOR_TOUCH   #Set the type of sensor
BrickPi.SensorType[SONAR_SENSOR] = TYPE_SENSOR_ULTRASONIC_CONT # Set up ultrsonic sensor
BrickPiSetupSensors()   #Send the properties of sensors to BrickPi
# test touch sensor
#left_90deg()
#right_90deg()
#run_touchSensor()

# test ultrasonic sensor
#run_sonarSensor()
#print get_distance()
#run_walkalongwall()
'''move_forward()
while True:
    BrickPiUpdateValues()'''
print "action1"
navigateToWaypoint(50.0,50.0)
time.sleep(0.5)
print "action2"
navigateToWaypoint(50.0,-20.0)
time.sleep(0.5)
print "action3"
navigateToWaypoint(0.0,0.0)
time.sleep(0.5)
#turn(45)
#time.sleep(0.5)
#turn(180)
#while not (bumper_left_hit() or bumper_right_hit()):
#for i in range(10):
#    BrickPiUpdateValues()
#    print BrickPi.Sensor[SONAR_SENSOR]
#    time.sleep(0.05)
'''def test_turn(degrees):
    motorRotateDegree([123,123],[-1.950*degrees,1.950*degrees],[LEFT_MOTOR,RIGHT_MOTOR])
test_turn(180)'''


