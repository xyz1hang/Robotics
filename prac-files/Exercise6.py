from BrickPi import *   #import BrickPi.py file to use BrickPi operations
from numpy import *
import random
import os
import threading 
from collections import Counter
from Exercise5v2 import *
    
LEFT_MOTOR = PORT_A
RIGHT_MOTOR = PORT_C
SONAR_MOTOR = PORT_B

LEFT_TOUCHSENSOR = PORT_3
RIGHT_TOUCHSENSOR = PORT_4
SONAR_SENSOR = PORT_2

# threadshold for depth histgram 
histThreshold = 5000000# initialisation
hit = False

# mutex = threading.Lock()
# condition = threading.Condition()

##################################################################################
''' This part is the motion of the robot'''
##################################################################################
def initialise():
    BrickPiSetup()  # setup the serial port for communication

    BrickPi.MotorEnable[LEFT_MOTOR] = 1 #Enable the Motor A
    BrickPi.MotorEnable[RIGHT_MOTOR] = 1 #Enable the Motor B
    BrickPi.MotorEnable[SONAR_MOTOR] = 1 #Enable the Motor which control the rotation of sonar sensor
    
    BrickPi.SensorType[LEFT_TOUCHSENSOR] = TYPE_SENSOR_TOUCH   #Set the type of sensor
    BrickPi.SensorType[RIGHT_TOUCHSENSOR] = TYPE_SENSOR_TOUCH   #Set the type of sensor
    BrickPi.SensorType[SONAR_SENSOR] = TYPE_SENSOR_ULTRASONIC_CONT # Set up ultrsonic sensor
    
    BrickPiSetupSensors()

def forward(distance):
    motorRotateDegree([100,115],[18.75*distance,18.25*distance],[LEFT_MOTOR,RIGHT_MOTOR])

def turn(degrees):
    motorRotateDegree([100,90],[-1*degrees,1*degrees],[LEFT_MOTOR,RIGHT_MOTOR])
    
def rotateSonarSensor(degrees):
    # BrickPi.MotorSpeed[SONAR_MOTOR] = 10
    # 0.0174532925
    motorRotateDegree([150],[degrees],[SONAR_MOTOR], SONAR_SENSOR_PORT)
    # motorRotateDegree([100],[0.0174532925],[SONAR_MOTOR])
    
def bumper_left_hit():
    """get left bumper sensor data
    """
    return BrickPi.Sensor[LEFT_TOUCHSENSOR]

def bumper_right_hit():
    """get right bumper sensor data
    """
    return BrickPi.Sensor[RIGHT_TOUCHSENSOR]

def get_distance_measurement():
    """get sonar sensor data
    """
    result = BrickPiUpdateValues()  # Ask BrickPi to update values for sensors/$
    value = 0
    if not result :
        value = BrickPi.Sensor[SONAR_SENSOR]     #BrickPi.Sensor[PORT] stores the value$
    time.sleep(.01)     # sleep for 10 ms
    return value

def rotateSonar(angle, direct):
    print "rotating " + str(angle)
    rotateSonarSensor(angle*direct)
        
def rotatePI(direct, ls=None):
    '''# 13 time "1 degree" rotate motorRotateDegree 
    # 80 time "1 degree" rotate motorRotateDegree
    degree = 40
    while degree > 0:
        
        measurements = []
        # make measurement 10 times and take the mean
        if ls != None:
            
        
        rotateSonarSensor(1.0*direct)
        #turn(0.03141926)
        degree -= 1
    
    # return ls'''

##################################################################################
''' Location Signature classes'''
##################################################################################
        
# Location signature class: stores a signature characterizing one location
class LocationSignature:
    def __init__(self, no_bins = 80):
        self.sig = [] # [0] * no_bins
        
    def print_signature(self):
        for i in range(len(self.sig)):
            print self.sig[i]

# --------------------- File management class ---------------
class SignatureContainer():
    def __init__(self, size = 5):
        self.size      = size; # max number of signatures that can be stored
        self.filenames = [];
        
        # Fills the filenames variable with names like loc_%%.dat 
        # where %% are 2 digits (00, 01, 02...) indicating the location number. 
        for i in range(self.size):
            self.filenames.append('loc_{0:02d}.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are 
    # used, it returns -1;
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1
            
        if (n >= self.size):
            return -1;
        else:    
            return n;

    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print "STATUS:  All signature files removed."
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])
            
    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)
            
        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(signature.sig[i]) + "\n"
            f.write(s)
        f.close();

    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
        ls = LocationSignature()
        filename = self.filenames[index]
        print ls.sig
        print filename
        if os.path.isfile(filename):
            #f = open(filename, 'r')
            with open(filename) as fp:
                for line in fp:
                    if (line != ''):
                        ls.sig.append(int(float(line.replace("\n", ""))))
            '''for i in range(ls.bins):
                s = f.readline()
                if (s != ''):
                    ls.sig.append(int(float(s.replace("\n", ""))))'''
                    #ls.sig[i] = int(s)
            #f.close();
            fp.close();
        else:
            print "WARNING: Signature does not exist."
        print ls.sig
        return ls
    
##################################################################################
''' Location Signature application '''
##################################################################################


##################################################################################
'''Thread which get distance measurement from sencer '''
##################################################################################
'''class ReadFromSensor(threading.Thread):
    def __init__(self, ls):
        super(ReadFromSensor, self).__init__()
        self._stop = threading.Event()
        self.ls = ls
        
    def run(self):
        
        # call barrier
        print "reading is acquiring"
        condition.acquire()
        print "reading is ready to notify"
        condition.notify()
        condition.release()
        
        # keep reading
        while True:
            measurements = []
            count = 5
            m = 0.0
            while count > 0:
                m = get_distance_measurement()
                measurements.append(m)
                count -= 1
                # print str(m)
                dis = int(mean(measurements))

            self.ls.sig.append(dis)
            
    def getResult(self):
        return self.ls
    
    def stop(self):
        self._stop.set()
        
    def stopped(self):
        return self._stop.isSet()'''

def shapeList(alist,size):
    list_size = len(alist)
    scale = float(list_size)/float(size)
    new_list = alist*3
    result = []
    for i in range(size):
        low_bound = int(round(scale*(i-1.5)+list_size))
        up_bound = int(round(scale*(i+1.5)+ list_size))
        value = median(new_list[low_bound:up_bound])
        result.append(value)
    return result

# FILL IN: spin robot or sonar to capture a signature and store it in ls
def characterize_location(ls, learning):
    # print "TODO:    You should implement the function that captures a signature."    
    '''for i in range(len(ls.sig)):
        ls.sig[i] = random.randint(0, 255)'''

        # rotatePI(1)
    
    # Innitual read thread
    '''read = ReadFromSensor(ls)
    read.start()
    
    # wait for the read thread to start
    print "main is acquiring"
    condition.acquire()
    print "main is waiting"
    condition.wait()
    print "main is running"'''
    
    # rotateSonar(860*2+100, -1)
    if learning:
        print "rotate to starting location"
        # rotateSonar(860, 1)
        motorRotateDegree([200],[6.8*180],[SONAR_MOTOR],[SONAR_SENSOR],ls,False)
        print "reading..."
        ls = motorRotateDegree([90],[(7.1*180)*2.0*(-1)],[SONAR_MOTOR],[SONAR_SENSOR],ls,True)
        ls.sig = shapeList(ls.sig,360)
        print len(ls.sig)
        motorRotateDegree([200],[7.2*180],[SONAR_MOTOR],[SONAR_SENSOR],ls,False)
    else:
        print "rotate to starting location"
        # rotateSonar(860, 1)
        motorRotateDegree([200],[6.8*180],[SONAR_MOTOR],[SONAR_SENSOR],ls,False)
        print "reading..."
        ls = motorRotateDegree([90],[(7.1*180)*2.0*(-1)],[SONAR_MOTOR],[SONAR_SENSOR],ls,True)
        ls.sig = shapeList(ls.sig,360)
        print len(ls.sig)
        motorRotateDegree([200],[7.2*180],[SONAR_MOTOR],[SONAR_SENSOR],ls,False)
        '''
        print "reading..."
        ls = motorRotateDegree([90],[(6.8*)*(-1)],[SONAR_MOTOR],[SONAR_SENSOR],ls,True)
        motorRotateDegree([200],[6.9*100],[SONAR_MOTOR],[SONAR_SENSOR],ls,False)'''
        '''global histThreshold
        histThreshold = len(ls.sig)*pow(5,2) if histThreshold == 0 else histThreshold'''
    
    # stop the reading thread
    '''ls = read.getResult()
    
    while not read.stopped():
        read.stop()
        
    print "reading thread stop called"
    read.join()
    print "condition released"
    condition.release()'''
    
    print "rotate back"
    # rotateSonar(860, 1)
    #motorRotateDegree([150],[880],[SONAR_MOTOR],ls,SONAR_SENSOR,False)
    #rotatePI(1)

# FILL IN: compare two signatures
def compare_signatures(ls_obs, ls_read):
    print "ls_obs size: " + str(len(ls_obs.sig))
    print "ls_read size: " + str(len(ls_read.sig))
    dist = 0
    #print "TODO:    You should implement the function that compares two signatures."
    # the number of signatures during observation might not be exactly the same as reading

    # double the previously reading
    '''new_ls_read = ls_read.sig
    new_ls_obs = ls_obs.sig
    corrList = correlate(new_ls_read*2, new_ls_obs, 'full')
    corrIdx = argsort(corrList)[::-1]
    idx = max(corrIdx[0:3])
    maxcorr = corrList[idx] 
    print idx
    idx = idx - len(new_ls_obs)
    print idx
    if idx > len(new_ls_read):
        idx = idx - len(new_ls_read)
    print idx
    scale = 360.0/float(len(new_ls_read))
    print "scale " + str(scale)
    print "degree: "+ str(scale*(idx+0.5))
    angle = -180 + scale*(idx + 0.5)'''
    freq_read = cal_freq2(ls_read.sig)
    freq_obs = cal_freq2(ls_obs.sig)
    freq_dif = sum(list(abs(array(freq_read)-array(freq_obs))))
    return freq_dif

def cal_freq1(alist):
    freq = [0]*255
    counter_list = Counter(alist).items()
    for i in range(len(counter_list)):
        freq[counter_list[i][0]] = counter_list[i][1]
    return freq


def cal_freq2(alist):
    freq = [0]*26
    for i in range(len(alist)):
        freq[int(alist[i]/10)] += 1
    return freq
# This function characterizes the current location, and stores the obtained 
# signature into the next available file.
def learn_location():
    ls = LocationSignature()
    characterize_location(ls, True)
    idx = signatures.get_free_index();
    if (idx == -1): # run out of signature files
        print "\nWARNING:"
        print "No signature file is available. NOTHING NEW will be learned and stored."
        print "Please remove some loc_%%.dat files.\n"
        return
    
    signatures.save(ls,idx)
    print "STATUS:  Location " + str(idx) + " learned and saved."
    
def cal_angle(ls_obs, ls_read):
    #print "TODO:    You should implement the function that compares two signatures."
    reads = ls_read.sig * 2
    obs = ls_obs.sig
    print len(ls_read.sig)
    print "ls_read     "+str(ls_read.sig)
    print len(ls_obs.sig)
    print "ls_obs      "+str(ls_obs.sig)
    min_distance = float('inf') 
    min_index = 0
    for i in range(len(reads)/2):
        distance = 0
        for j in range(len(obs)):
            distance += sqrt(power((reads[i+j] - obs[j]),2))
        if distance < min_distance:
            min_distance = distance
            min_index = i
    if min_index > len(ls_read.sig):        
        min_index = min_index - len(ls_read.sig)
    
    print "min_distance: "+ str(min_distance)
    print "min_index: " + str(min_index)
    scale = 360.0/float(len(ls_read.sig))
    angle = -scale*(min_index+0.5)
    if angle < -180:
        angle = angle + 360
    return [min_distance,angle]

# This function tries to recognize the current location.
# 1.   Characterize current location
# 2.   For every learned locations
# 2.1. Read signature of learned location from file
# 2.2. Compare signature to signature coming from actual characterization
# 3.   Retain the learned location whose minimum distance with
#      actual characterization is the smallest.
# 4.   Display the index of the recognized location on the screen
def recognize_location():
    ls_obs = LocationSignature();
    characterize_location(ls_obs, False);

    best_idx = -1
    currentMax = histThreshold
    
    # FILL IN: COMPARE ls_read with ls_obs and find the best match
    for idx in range(signatures.size):
        print "STATUS:  Comparing signature " + str(idx) + " with the observed signature."
        ls_read = signatures.read(idx);
        result    = compare_signatures(ls_obs, ls_read)
        
        print "checking location: " + str(idx)
        
        if result < currentMax:
            print currentMax
            currentMax = result
            best_idx = idx

    print "At location: " + str(best_idx)
    if best_idx != -1:
        ls_read = signatures.read(best_idx)
        [min_distance, angle] = cal_angle(ls_obs,ls_read) # need to initial a minimum distance Threshold to decide whether this is the location
        print "min_distance  " + str(min_distance)
        print "angle  "+ str(angle)
    else:
        print "Not in any location"
        
    
def cal_best_path(goals,path_idx,locIdx):
    idx = path_idx.index(locIdx)
    best_path = []
    best_path.extend(path_idx[idx:])
    best_path.extend(path_idx[0:idx])
    best_path.append(locIdx)
    path = []
    for i in range(len(best_path)):
        path.append(goals[best_path[i]])
    return path

def estCurrentlocation():
    current_x = 0
    current_y = 0
    current_theta = 0
    for i in range(particles.n):
        current_x = current_x + particles.data[i][0]*particles.data[i][3]
        current_y = current_y + particles.data[i][1]*particles.data[i][3]
        current_theta = current_theta + particles.data[i][2]*particles.data[i][3]
    print "Current position " + str([current_x,current_y,current_theta*180/math.pi])
    
    return [current_x, current_y, current_theta]
    
def calibration(x,y):
    '''function to return the degree to rotate
       and distance to move in order to get to
       given waypoint
    '''
    
    [current_x, current_y, current_theta] = estCurrentlocation()
    
    print "Navigate to " + str([x,y])
    
    distance = pow(pow(x-current_x,2)+pow(y-current_y,2),0.5)

    dif_y = float(round(y,3)-round(current_y,3))
    dif_x = float(round(x,3)-round(current_x,3))
    
    if dif_x == 0:
        if y > current_y:
            degree = math.pi/2 - current_theta
        elif y < current_y:
            degree = -math.pi/2 - current_theta
    else:
        degree = math.atan(dif_y/dif_x)
        if dif_y >= 0 and dif_x >0:
            degree = degree - current_theta
        elif dif_y >= 0 and dif_x< 0:
            degree = degree - current_theta + math.pi
        elif dif_y <=0  and dif_x > 0:
            degree = degree - current_theta
        elif dif_y <= 0 and dif_x < 0:
            degree = degree - current_theta - math.pi
        if degree > math.pi:
            degree -= math.pi*2
        elif degree < -math.pi:
            degree += math.pi*2
            
    return [degree, distance]

def navigateToWaypoint(x, y):
    '''navigate to waypoint from current location
       based on necessary rotating degree and distance to
       move forward, which are generated by calibration
    '''
    
    [degree, distance] = calibration(x, y)
    
    # turn to the right direction
    # when beginning navigating to a new waypoint
    print "turn " + str(degree/math.pi*180)
    turn(degree/math.pi*180)
    particles.draw()
    # calibrate to see if it needs to further rotate
    motion = Coordinate(rotateAngle = degree)
    renew_particles(motion, "turn")
    [degree, distance] = calibration(x, y)
    
    global hit
    while distance > 2:
        
        if (bumper_left_hit() or bumper_right_hit()):
                hit = True
                break
        
        print "distance " + str(distance)
        # while the degree it think it needs to rotate not
        # too far away from 0 i.e not trivial
        while abs(degree) > 0.05:
            print "turn " + str(degree/math.pi*180)
            # turn
            turn(degree/math.pi*180)
            particles.draw()            
            # calibrate to see if it needs to further rotate
            motion = Coordinate(rotateAngle = degree)
            renew_particles(motion, "turn")
            [degree, distance] = calibration(x, y)
            time.sleep(0.5)
            
        print "forward " + str(distance)

        if distance > 20:
            forward(20)
            particles.draw()
            motion = Coordinate(forwardDis = 20)
        else:
            forward(distance)
            particles.draw()
            motion = Coordinate(forwardDis = distance)

        renew_particles(motion, "forward")    
        [degree, distance] = calibration(x, y)
        time.sleep(0.5)
        print "\n"
    
            
if __name__ == "__main__":
    
    initialise()
    
    signatures = SignatureContainer(5);
    # signatures.delete_loc_files()
    #print "learning..."
    #learn_location();
    # the file stored in the order or point 5 2 4 1 7
    goals = [(126,168),(180,30),(126,54),(84,30),(30,54)]
    # path = [1 2 5 4 7]
    path_idx = [3,1,0,2,4]

    
    
    '''# 1. recognize current location and current angle'''
    print "recognizing..."
    #[locIdx,angle] = recognize_location()
    
    
    particles = pds.Particles(20,20,1.3)
    particles.draw()
    ''' # 2. according to 5 destination and current status calculate the best move'''
    ''' Calculate the path'''
    best_path = cal_best_path(goals,path_idx,locIdx)

    #current location and direction
    current_x = goals[locIdx][0]
    current_y = goals[locIdx][1]
    current_theta = angle
    ''' # 3. start to move and update current location and current direction using MCL'''
    path_pointer = 0
    while path_pointer < len(best_path):
        ex5.navigateToWaypoint(best_path[path_pointer]) #TODO finish navigate to function
        '''# 4. if acheive one destination then shine the light'''
        
        
        
        path_pointer += 1
    

