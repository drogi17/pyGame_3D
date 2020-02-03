import pygame.font as pygame_font
import datetime

def show_fps(wind, f_fps, f_fps_now, f_datetime_now, text_pos):
    f_fps_now += 1
    datetime_now_1 = datetime.datetime.today().strftime("%S")
    if datetime_now_1 != f_datetime_now:
        f_fps = f_fps_now
        f_fps_now = 0
        f_datetime_now = datetime_now_1[:]
    fps_font = pygame_font.Font(None, 20)
    fps_text = fps_font.render('FPS: ' + str(f_fps), True, (225, 225, 225))
    wind.blit(fps_text, text_pos)
    return wind, f_fps, f_fps_now, f_datetime_now