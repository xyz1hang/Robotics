from BrickPi import *

LEFT_MOTOR = PORT_A
RIGHT_MOTOR = PORT_B

LEFT_TOUCHSENSOR = PORT_3
RIGHT_TOUCHSENSOR = PORT_1
SONAR_SENSOR = PORT_2

stdDev = 1.4
likeliOffset = 0.1
likeliThreshold = 0.2
angleThreshold = 0.558505361 # 32 degree
numOfParticles = 100

angleChecks = 0 # counter for angle check reported from all particles

def initialise():
    BrickPiSetup()  # setup the serial port for communication

    BrickPi.MotorEnable[LEFT_MOTOR] = 1 #Enable the Motor A
    BrickPi.MotorEnable[RIGHT_MOTOR] = 1 #Enable the Motor B

    BrickPi.SensorType[LEFT_TOUCHSENSOR] = TYPE_SENSOR_TOUCH   #Set the type of sensor
    BrickPi.SensorType[RIGHT_TOUCHSENSOR] = TYPE_SENSOR_TOUCH   #Set the type of sensor
    BrickPi.SensorType[SONAR_SENSOR] = TYPE_SENSOR_ULTRASONIC_CONT # Set up ultrsonic sensor
    BrickPiSetupSensors()
    
if __name__ == "__main__":
    initialise()
    '''BrickPi.MotorSpeed[LEFT_MOTOR] = 85  #Set the speed of MotorA (-255 to 255)
    BrickPi.MotorSpeed[RIGHT_MOTOR] = 90  #Set the speed of MotorB (-255 to 255)
    while True:
        BrickPiUpdateValues()'''
    #motorRotateDegree([100,95],[18.75*20,18.75*20],[LEFT_MOTOR,RIGHT_MOTOR])
    motorRotateDegree([105,110],[-1.805*90,1.805*90],[LEFT_MOTOR,RIGHT_MOTOR])
    print "test"
    
