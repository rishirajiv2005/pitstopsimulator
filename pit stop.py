from time import sleep
import pygame
from pitstopsensors import *
from math import floor, sin, cos, pi

SENSOR_CFG_FILE = "./sensors.txt"

sensors_file = open(SENSOR_CFG_FILE, "r")
sensors_list = sensors_file.readlines()
sensors_dict = {}

for line in sensors_list:
    keyval = line.replace(" ","").split("=")
    sensors_dict[keyval[0]] = int(keyval[1])
    
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1600, 900))
dt = 0
elapsed = 0

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
    
    global screen, dt, elapsed
    clock = pygame.time.Clock()
    clock_font = pygame.font.Font(pygame.font.match_font("7-segment", bold=True, italic=False), 96)
#     clock_text = clock_font.render("00:00:00", True, (255, 255, 255))
#     clock_rect = clock_text.get_rect()
#     clock_rect.center = [screen.get_width() *0.5, screen.get_height()*0.5]
    
    indicators_font = pygame.font.Font(pygame.font.match_font("sans", bold=True, italic=False), 24)
#     fwp_text = indicators_font.render("FW PRESENT", True, (0, 255, 0))
#     fwp_rect = fwp_text.get_rect()
#     fwp_rect.center = [screen.get_width() *0.33333, screen.get_height()*0.25]
    
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
        
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0,0,128))
        
        
        millisc = floor((elapsed - floor(elapsed)) * 100)
        seconds = floor(elapsed) % 60
        minutes = floor(elapsed / 60)
        timestr = str(minutes).rjust(2, '0') + ":" + str(seconds).rjust(2, '0') + ":" + str(millisc).rjust(2, '0')
        clock_text = clock_font.render(timestr, True, (255, 255, 255))
        clock_rect = clock_text.get_rect()
        clock_rect.center = [screen.get_width() *0.5, screen.get_height()*0.875]
        screen.blit(clock_text, clock_rect)
        
        fwp_text = indicators_font.render("FW PRESENT: " + str(front_wheel.present), True, (255* int(not front_wheel.present), 255 * int(front_wheel.present), 0))
        fwp_rect = fwp_text.get_rect()
        fwp_rect.center = [screen.get_width() *0.25, screen.get_height()*0.25]
        screen.blit(fwp_text, fwp_rect)
        
        fwl_text = indicators_font.render("FW LOCKED: " + str(front_wheel.locked), True, (255* int(not front_wheel.locked), 255 * int(front_wheel.locked), 0))
        fwl_rect = fwl_text.get_rect()
        fwl_rect.center = [screen.get_width() *0.25, screen.get_height()*0.30]
        screen.blit(fwl_text, fwl_rect)
        
        rwp_text = indicators_font.render("RW PRESENT: " + str(rear_wheel.present), True, (255* int(not rear_wheel.present), 255 * int(rear_wheel.present), 0))
        rwp_rect = rwp_text.get_rect()
        rwp_rect.center = [screen.get_width() *0.75, screen.get_height()*0.25]
        screen.blit(rwp_text, rwp_rect)
        
        rwl_text = indicators_font.render("RW LOCKED: " + str(rear_wheel.locked), True, (255* int(not rear_wheel.locked), 255 * int(rear_wheel.locked), 0))
        rwl_rect = rwl_text.get_rect()
        rwl_rect.center = [screen.get_width() *0.75, screen.get_height()*0.30]
        screen.blit(rwl_text, rwl_rect)
        
        print(screen.get_width())
       
        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
        elapsed += dt
    

idle()