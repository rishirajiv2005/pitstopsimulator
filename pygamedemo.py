# Example file showing a circle moving on screen
import pygame
from math import floor, sin, cos, pi

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

elapsed = 0

# pygame.font.get_default_font()
font = pygame.font.Font(pygame.font.match_font("7-segment", bold=True, italic=False), 96)
text = font.render("00:00:00", True, (255, 255, 255))
textRect = text.get_rect()
textRect.center = (screen.get_width() *0.5, screen.get_height()*0.5)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("blue")
    
    
    millisc = floor((elapsed - floor(elapsed)) * 100)
    seconds = floor(elapsed) % 60
    minutes = floor(elapsed / 60)
    
    timestr = str(minutes).rjust(2, '0') + ":" + str(seconds).rjust(2, '0') + ":" + str(millisc).rjust(2, '0')
    
    text = font.render(timestr, True, (255, 255, 255))
    textRect = text.get_rect()
    
    screen.blit(text, textRect)
    


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    elapsed += dt

pygame.quit()