import os, sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
pygame.init()
import config
import datetime
from time import sleep
from modules.fps_get import show_fps
from modules.player import camera, control
from modules.world import world

world                   = world('Simple')
SCREEN_RESOLUTION       = config.SCREEN_RESOLUTION
if config.SET_NATIVE_RESOLUTION:
	SCREEN_RESOLUTION   = config.NATIVE_RESOLUTION
else:
	SCREEN_RESOLUTION   = config.SCREEN_RESOLUTION
GRAB_MODE               = config.GRAB_MODE
center_x                = SCREEN_RESOLUTION[0]//2
center_y                = SCREEN_RESOLUTION[1]//2
camera                  = camera(pos=[0, 0, -2], resol=SCREEN_RESOLUTION)
pygame.event.get()
pygame.mouse.get_rel()
pygame.mouse.set_visible(0)
pygame.event.set_grab(GRAB_MODE)


################# Добавление моделек на карту #################
world.add_axes(color=(255, 0, 0))   #   Добавить подсветку координаты x, y, z
# world.add_obj_model('models/Apple.obj', resize=0.4, color=(0, 225, 225)) #    Добавить модельку и изменить размер
# world.save_world() #   Загрузить мир
world.load_world('worlds/Simple/') #   Загрузить мир


#################    отображение окна     #################
pygame.display.set_caption('GAME')                     # Обьявление Имени окна
win = pygame.display.set_mode(SCREEN_RESOLUTION)       # Размер экрана
if config.FUULSCREEN:                                  #\   FUUL SCREEN MODE
    pygame.display.toggle_fullscreen()                 #/   FUUL SCREEN MODE


#################          FPS 0          #################
datetime_now = datetime.datetime.today().strftime("%S") # Обьявление времени при fps = 0
fps     = 0                                             # Обьявление нулевого fps
fps_now = 0                                             # Обьявление нулевого fps счетчика
clock = pygame.time.Clock()                             # Обьявление clock


################# alex6446 ########################
def clip_z (points):
    near = 0.001
    k = (near-points[0][2])/(points[1][2]-points[0][2])
    x = k*(points[1][0]-points[0][0])+points[0][0]
    y = k*(points[1][1]-points[0][1])+points[0][1]
    return [x, y, near]
    

def conv_pos (cords):
    x = cords[0]*(center_x/cords[2])
    y = cords[1]*(center_x/cords[2])
    return [x, y]

in_progress = True # Начать работу цикла
if not '--no-logo' in sys.argv:
    print('MADE BY: @drogi17 & @Alexey6446')
    win.fill((0, 0, 0))
    name_font = pygame.font.Font(None, 400)
    name_text = name_font.render('3D GAME', True, (225, 225, 225))
    name_pos = (center_x-center_x/1.6, center_y-center_y/4)
    win.blit(name_text, name_pos)
    pygame.display.update()
    sleep(2)
while in_progress:
    win.fill((0, 0, 0))                                          # Залить черным цветом
    GRAB_MODE, camera, in_progress =  control(GRAB_MODE, camera) # Контролировать положение камеры
    for block in world.blocks:                                   # Начать отображение блоков
        for conn_ct in block['connections']:
            points_array2d = []
            points = []
            count = 0
            for conn_point in conn_ct:
                points.append(block['cube_points_dict'][conn_ct[count]])
                count += 1
            transformed = []
            point_nomb = 0
            while point_nomb < len(points):
                transformed = []
                if point_nomb == len(points)-1:
                    points_2 = [points[point_nomb], points[0]]
                else:
                    points_2 = [points[point_nomb], points[point_nomb+1]]
                for point in points_2:
                    x = point[0] - camera.pos[0] + block['pos'][0]
                    y = point[1] - camera.pos[1] + block['pos'][1]
                    z = point[2] - camera.pos[2] + block['pos'][2]
                    x, z = camera.rotation_camera((x, z), camera.angle[0])
                    y, z = camera.rotation_camera((y, z), camera.angle[1])
                    transformed.append([x, y, z])
                if transformed[0][2] > 0 and transformed[1][2] > 0:
                    points_array2d = [conv_pos(transformed[0]), 
                                      conv_pos(transformed[1])]
                elif transformed[0][2] > 0:
                    points_array2d = [conv_pos(transformed[0]), 
                                      conv_pos(clip_z(transformed))]
                elif transformed[1][2] > 0:
                    points_array2d = [conv_pos(clip_z(transformed)), 
                                      conv_pos(transformed[1])]
                if len(points_array2d) == 2:
                    points_array2d = [[x+y for x, y in zip(points_array2d[0], [center_x, center_y])], 
                                     [ x+y for x, y in zip(points_array2d[1], [center_x, center_y])]] 
                    if config.DRAW_POINTS:
                        pygame.draw.circle(win, block['color'], (round(points_array2d[0][0]), round(points_array2d[0][1])), 4)
                        pygame.draw.circle(win, block['color'], (round(points_array2d[1][0]), round(points_array2d[1][1])), 4)
                    pygame.draw.line(win, block['color'], points_array2d[0], points_array2d[1], 1)
                point_nomb += 1
    if config.SHOW_POINTER:
        if config.CURSOR_TYPES[config.CURSOR_TYPE] == 1:
            pygame.draw.circle(win, config.POINTER_COLOR, (round(center_x), round(center_y)), 2)
        elif config.CURSOR_TYPES[config.CURSOR_TYPE] == 2:
            pass
    ########################################## New frame ##########################################
    win, fps, fps_now, datetime_now = show_fps(win, fps, fps_now, datetime_now, config.FPS_POSITION)
    pygame.display.update()
    pygame.display.flip()
    clock.tick(config.FPS_MAX)