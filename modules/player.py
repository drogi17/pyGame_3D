import pygame
import math

class camera:           #Класс камеры
    def __init__(self, pos=[0, 0, 0], angle=[0, 0, 0], resol=(500, 500)):
        self.resol  = resol
        self.pos    = pos
        self.angle  = angle

    def move_camera(self, key):           #Движение камерой
        speed = 0.1
        x = math.sin(self.angle[0])*speed
        y = math.cos(self.angle[0])*speed
        
        if key[pygame.K_SPACE]:
            self.pos[1] += 0.1
        if key[pygame.K_LSHIFT]:
            self.pos[1] -= 0.1

        if key[pygame.K_w]:
            self.pos[2] += x
            self.pos[0] += y
        if key[pygame.K_s]:
            self.pos[2] -= x
            self.pos[0] -= y
        if key[pygame.K_a]:
            self.pos[2] -= y
            self.pos[0] += x
        if key[pygame.K_d]:
            self.pos[2] += y
            self.pos[0] -= x

    def events_camera(self, event):             #Движение мышью
        if event.type == pygame.MOUSEMOTION:
            x, y = event.rel
            x   /= self.resol[0]//2
            y   /= self.resol[1]//2
            self.angle[0] += x
            self.angle[1] += y

    def rotation_camera(self, pos, radian):     # Выщивытание поворота камеры
        x = pos[0]
        y = pos[1]
        sin = math.sin(radian)
        cos = math.cos(radian)
        x_r = y*cos - x*sin
        y_r = x*cos + y*sin
        return x_r, y_r

def control(GRAB_MODE, camera_control, in_progress=True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            in_progress = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                in_progress = False
            if event.key == pygame.K_l:
                if GRAB_MODE == 0:
                    GRAB_MODE = 1
                elif GRAB_MODE == 1:
                    GRAB_MODE = 0
                pygame.event.set_grab(GRAB_MODE)
        camera_control.events_camera(event)
    camera_control.move_camera(pygame.key.get_pressed())
    return GRAB_MODE, camera_control, in_progress