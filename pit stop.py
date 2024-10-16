import pygame, cv2
from time import sleep
from pitstopsensors import *
from math import floor, sin, cos, pi

SENSOR_CFG_FILE = "./sensors.txt"
INTRO_VIDEO_FILE = "./pit stop mockup short.mp4"

sensors_file = open(SENSOR_CFG_FILE, "r")
sensors_list = sensors_file.readlines()
sensors_dict = {}

for line in sensors_list:
    keyval = line.replace(" ","").split("=")
    sensors_dict[keyval[0]] = int(keyval[1])
    
# pygame setup
pygame.init()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)   # initializes full-screen display
#screen = pygame.display.set_mode((1280, 720))
dt = 0
elapsed = 0

def idle():
    ## play attract video from here
    global screen
    
    idle_font = pygame.font.Font(pygame.font.match_font("paradiso", bold=True, italic=False), 96)   # displays title text in center of screen
    screen.fill((128,0,0))
    idle_text = idle_font.render("Indy 500 Pit Stop Simulator", True, (255,255,255))
    idle_rect = idle_text.get_rect()
    idle_rect.center = [screen.get_width() *0.5, screen.get_height()*0.5]
    screen.blit(idle_text, idle_rect)
    pygame.display.flip()
    
    global sensors_dict
    game_start_input = Button(sensors_dict["GAME_START"])
    while True:
        #print("idling")

        if game_start_input.value:
            #print("countdown")
            countdown()
        
        sleep(1)

def countdown():
    global screen
    ## play countdown video from here
    
    
    ## find some multimedia library that can call back to here when the video is done playing, then initiate the game
    ## for now there is just gonna be a cute little for loop here
    
    ## using cv2
    
    intro_video = cv2.VideoCapture(INTRO_VIDEO_FILE)
    success, video_frame = intro_video.read()
    playback = success
    clock = pygame.time.Clock()
    
#    fps = video.get(cv2.CAP_PROP_FPS)
    while playback:
        clock.tick(23.976024)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playback = false
        success, video_frame = intro_video.read()
        if success:
            #print(str(video_frame.shape[1::-1]))
            video_blit = pygame.image.frombuffer(video_frame.tobytes(), video_frame.shape[1::-1], "BGR")   # scales and displays video frames to fit the screen
            video_blit = pygame.transform.scale(video_blit, (screen.get_width(),screen.get_height()))
        else:
            print("huh")
            playback = False
        screen.blit(video_blit, (0,0))
        pygame.display.flip()
                
    
    
    
    countdown_font = pygame.font.Font(pygame.font.match_font("paradiso", bold=True, italic=False), 160)   # displays countdown text in the center of the screen
    screen.fill((128,0,0))
    pygame.display.flip()
    
    for i in range(1, 4):
        screen.fill((128,0,0))
        cd_text = countdown_font.render(str(4- i), True, (255,255,255))
        cd_rect = cd_text.get_rect()
        cd_rect.center = [screen.get_width() *0.5, screen.get_height()*0.5]
        screen.blit(cd_text, cd_rect)
        pygame.display.flip()
        sleep(1)
    
    gameloop()


def gameloop():
    ## main gameplay loop
    
    global sensors_dict
    front_wheel = wheel("Front", sensors_dict["WHEEL_F_PRESENT"], sensors_dict["WHEEL_F_LOCKED"], sensors_dict["WHEEL_F_NEW"])
    rear_wheel = wheel("Rear", sensors_dict["WHEEL_R_PRESENT"], sensors_dict["WHEEL_R_LOCKED"], sensors_dict["WHEEL_R_NEW"])
    fuel = fueltank("Fuel Tank", sensors_dict["FUEL_PROBE"])
    
    global screen, dt, dtu, elapsed
    clock = pygame.time.Clock()
    clock_font = pygame.font.Font(pygame.font.match_font("7-segment", bold=True, italic=False), 128)
    
    indicators_font = pygame.font.Font(pygame.font.match_font("paradiso", bold=True, italic=False), 24)
    clock_font_comp = pygame.font.Font(pygame.font.match_font("7-segment", bold=True, italic=False), 48)
    
    fc = rc = tc = False
    fc_time = rc_time = tc_time = "--:--:--"
    
    while True:
        front_wheel.update()
        rear_wheel.update()
        fuel.update()
        
        
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0,0,128))
        
        
        if (not (fc and rc and tc)):
            millisc = floor((elapsed - floor(elapsed)) * 100)
            seconds = floor(elapsed) % 60
            minutes = floor(elapsed / 60)
            timestr = str(minutes).rjust(2, '0') + ":" + str(seconds).rjust(2, '0') + ":" + str(millisc).rjust(2, '0')
        clock_text = clock_font.render(timestr, True, (255, 255, 255))
        clock_rect = clock_text.get_rect()
        clock_rect.center = [screen.get_width() *0.5, screen.get_height()*0.875]
        screen.blit(clock_text, clock_rect)

        # controls and displays font effectively
        fwp_text = indicators_font.render("FW PRESENT: " + str(front_wheel.get_present()), True, (255* int(not front_wheel.get_present()), 255 * int(front_wheel.get_present()), 0))
        fwp_rect = fwp_text.get_rect()
        fwp_rect.center = [screen.get_width() *0.25, screen.get_height()*0.25]
        screen.blit(fwp_text, fwp_rect)
        
        fwl_text = indicators_font.render("FW LOCKED: " + str(front_wheel.get_locked()), True, (255* int(not front_wheel.get_locked()), 255 * int(front_wheel.get_locked()), 0))
        fwl_rect = fwl_text.get_rect()
        fwl_rect.center = [screen.get_width() *0.25, screen.get_height()*0.30]
        screen.blit(fwl_text, fwl_rect)
        
        fwn_text = indicators_font.render("FW NEW: " + str(front_wheel.new), True, (255* int(not front_wheel.new), 255 * int(front_wheel.new), 0))
        fwn_rect = fwn_text.get_rect()
        fwn_rect.center = [screen.get_width() *0.25, screen.get_height()*0.35]
        screen.blit(fwn_text, fwn_rect)
        
        fwv_text = indicators_font.render("FW VALID: " + str(front_wheel.get_valid()), True, (255* int(not front_wheel.get_valid()), 255 * int(front_wheel.get_valid()), 0))
        fwv_rect = fwv_text.get_rect()
        fwv_rect.center = [screen.get_width() *0.25, screen.get_height()*0.40]
        screen.blit(fwv_text, fwv_rect)
        
        fwc_text = indicators_font.render("FW COMPLETE: " + str(front_wheel.get_complete()), True, (255* int(not front_wheel.get_complete()), 255 * int(front_wheel.get_complete()), 0))
        fwc_rect = fwc_text.get_rect()
        fwc_rect.center = [screen.get_width() *0.25, screen.get_height()*0.45]
        screen.blit(fwc_text, fwc_rect)
        
        rwp_text = indicators_font.render("RW PRESENT: " + str(rear_wheel.get_present()), True, (255* int(not rear_wheel.get_present()), 255 * int(rear_wheel.get_present()), 0))
        rwp_rect = rwp_text.get_rect()
        rwp_rect.center = [screen.get_width() *0.75, screen.get_height()*0.25]
        screen.blit(rwp_text, rwp_rect)
        
        rwl_text = indicators_font.render("RW LOCKED: " + str(rear_wheel.get_locked()), True, (255* int(not rear_wheel.get_locked()), 255 * int(rear_wheel.get_locked()), 0))
        rwl_rect = rwl_text.get_rect()
        rwl_rect.center = [screen.get_width() *0.75, screen.get_height()*0.30]
        screen.blit(rwl_text, rwl_rect)
        
        rwn_text = indicators_font.render("RW NEW: " + str(rear_wheel.new), True, (255* int(not rear_wheel.new), 255 * int(rear_wheel.new), 0))
        rwn_rect = rwn_text.get_rect()
        rwn_rect.center = [screen.get_width() *0.75, screen.get_height()*0.35]
        screen.blit(rwn_text, rwn_rect)
        
        rwv_text = indicators_font.render("RW VALID: " + str(rear_wheel.get_valid()), True, (255* int(not rear_wheel.get_valid()), 255 * int(rear_wheel.get_valid()), 0))
        rwv_rect = rwv_text.get_rect()
        rwv_rect.center = [screen.get_width() *0.75, screen.get_height()*0.40]
        screen.blit(rwv_text, rwv_rect)
        
        rwc_text = indicators_font.render("RW COMPLETE: " + str(rear_wheel.get_complete()), True, (255* int(not rear_wheel.get_complete()), 255 * int(rear_wheel.get_complete()), 0))
        rwc_rect = rwc_text.get_rect()
        rwc_rect.center = [screen.get_width() *0.75, screen.get_height()*0.45]
        screen.blit(rwc_text, rwc_rect)
        
        if ((not fc) and front_wheel.get_complete()):
            fc = True
            fc_time = timestr
        if ((not rc) and rear_wheel.get_complete()):
            rc = True
            rc_time = timestr
        
        clock_fc_text = clock_font_comp.render(fc_time, True, (255, 255, 255))
        clock_fc_rect = clock_fc_text.get_rect()
        clock_fc_rect.center = [screen.get_width() *0.25, screen.get_height()*0.675]
        screen.blit(clock_fc_text, clock_fc_rect)
        
        clock_rc_text = clock_font_comp.render(rc_time, True, (255, 255, 255))
        clock_rc_rect = clock_rc_text.get_rect()
        clock_rc_rect.center = [screen.get_width() *0.75, screen.get_height()*0.675]
        screen.blit(clock_rc_text, clock_rc_rect)
        
        tp_text = indicators_font.render("FUEL HOSE INSERTED: " + str(fuel.get_probe()), True, (255* int(not fuel.get_probe()), 255 * int(fuel.get_probe()), 0))
        tp_rect = tp_text.get_rect()
        tp_rect.center = [screen.get_width() *0.5, screen.get_height()*0.25]
        screen.blit(tp_text, tp_rect)
        
        tf_text = indicators_font.render("FUEL TANK FULL: " + str(fuel.get_full()), True, (255* int(not fuel.get_full()), 255 * int(fuel.get_full()), 0))
        tf_rect = tf_text.get_rect()
        tf_rect.center = [screen.get_width() *0.5, screen.get_height()*0.30]
        screen.blit(tf_text, tf_rect)
        
        tl_text = indicators_font.render("FUEL TANK LEVEL: " + str(floor(fuel.get_level())) +"%", True, (0,255,0))
        tl_rect = tf_text.get_rect()
        tl_rect.center = [screen.get_width() *0.5, screen.get_height()*0.35]
        screen.blit(tl_text, tl_rect)
        
        if ((not tc) and fuel.get_full()):
            tc = True
            tc_time = timestr

        # shows elapsed time in the game
        clock_tc_text = clock_font_comp.render(tc_time, True, (255, 255, 255))
        clock_tc_rect = clock_fc_text.get_rect()
        clock_tc_rect.center = [screen.get_width() *0.5, screen.get_height()*0.675]
        screen.blit(clock_tc_text, clock_tc_rect)
       
        # flip() the display to put your work on screen
        pygame.display.flip()
        

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000
        elapsed += dt
    

idle()
