import queue
import pygame
from pygame.locals import *

class Utilities:
    def leftClick(self):
        mouse = pygame.mouse.get_pressed()
        click = False

        if mouse[0]: # mouse[0] зберігає стан кліку в системі
            click = True
    
        return click
    
    def mouseCoords(self):
        pos = pygame.mouse.get_pos() # зчитування позиції мишки
        return pos