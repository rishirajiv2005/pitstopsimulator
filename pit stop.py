from time import *
import guizero
from pitstopsensors import *

game_start = 0
wheel_f_on = 1
wheel_f_lk = 1
wheel_r_on = 1
wheel_r_lk = 1
fuel = 0

def idle():
    ## play attract video from here
    
    global game_start
    while True:
        print("idling")
        game_start = bool(int(input("start? ")))
        if game_start == 1:
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
    ## for now there will be simulacrums of the input sensors
    
    front_wheel = wheel("Front")
    rear_wheel = wheel("Rear")
    main_tank = fueltank("Fuel Tank")
    
    while True:
        front_wheel.set_present()
        front_wheel.set_lock()
        front_wheel.set_new()
        
        rear_wheel.set_present()
        rear_wheel.set_lock()
        rear_wheel.set_new()
        
        
        ## validation func calls go here
    

idle()