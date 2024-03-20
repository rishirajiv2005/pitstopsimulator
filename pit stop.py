from time import *
#import guizero
from pitstopsensors import *

SENSOR_CFG_FILE = "./sensors.txt"

sensors_file = open(SENSOR_CFG_FILE, "r")
sensors_list = sensors_file.readlines()
sensors_dict = {}

for line in sensors_list:
    keyval = line.replace(" ","").split("=")
    sensors_dict[keyval[0]] = int(keyval[1])


def idle():
    ## play attract video from here
    
    global sensors_dict
    game_start_input = Button(sensors_dict["GAME_START"])
    while True:
        print("idling")

        if game_start_input.value:
            print("countdown")
            countdown()
        
        sleep(1)

def countdown():
    ## play coutndown video from here
    
    
    ## find some multimedia library that can call back to here when the video is done playing, then initiate the game
    ## for now there is just gonna be a cute little for loop here
    
    for i in range(1, 4):
        print(4 - i)
        sleep(1)
    
    gameloop()


def gameloop():
    ## main gameplay loop
    
    global sensors_dict
    front_wheel = wheel("Front", sensors_dict["WHEEL_F_PRESENT"], sensors_dict["WHEEL_F_LOCKED"], sensors_dict["WHEEL_F_NEW"])
    rear_wheel = wheel("Rear", sensors_dict["WHEEL_R_PRESENT"], sensors_dict["WHEEL_R_LOCKED"], sensors_dict["WHEEL_R_NEW"])
    main_tank = fueltank("Fuel Tank", sensors_dict["FUEL_PROBE"])
    
    while True:
        front_wheel.set_present()
        front_wheel.set_lock()
        front_wheel.set_new()
        
        rear_wheel.set_present()
        rear_wheel.set_lock()
        rear_wheel.set_new()
        
        #print("fw present: " + str(front_wheel.present) + " fw locked: " + str(front_wheel.locked) + " fw new: " + str(front_wheel.new))
        #print("rw present: " + str(rear_wheel.present) + " rw locked: " + str(rear_wheel.locked) + " rw new: " + str(rear_wheel.new))
        
        ## validation func calls go here
    

idle()