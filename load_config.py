import tkinter as tk
import os, sys
root = tk.Tk()
CURSOR_TYPES                = {
    'point': 1,
    'axis': 2
}

def load_config(file, cfg_settings):
    if os.path.exists(file):
        with open(file, 'r') as f:
            for line in f.readlines():
                coments = line.find('#')
                if coments != -1:
                    line = line[:coments]
                line = str(line).replace('\n', '')
                setting = str(line).replace(' ', '').replace('  ', '').split('=')
                if len(setting) > 1:
                    if setting[1] == 'False':
                        setting[1] = False
                    elif setting[1] == 'True':
                        setting[1] = True
                    elif str(setting[1]).isdigit():
                        setting[1] = int(setting[1])
                    elif ',' in setting[1]:
                        array = str(setting[1]).split(',')
                        nomb = 0
                        while nomb <= len(array)-1:
                            if str(array[nomb]).isdigit():
                                array[nomb] = int(array[nomb])
                            nomb += 1
                        setting[1] = array
                    if setting[0] in cfg_settings.cfg_dict:
                        cfg_settings.cfg_dict[setting[0]] = setting[1]
        return cfg_settings
    else:
        print('default.cfg not found')
        sys.exit()

class Config:
    cfg_dict = {
    'SCREEN_RESOLUTION': (800, 800),
    'NATIVE_RESOLUTION': (root.winfo_screenwidth(), root.winfo_screenheight()),
    'SET_NATIVE_RESOLUTION': False,
    'FPS_MAX': 60,
    'FPS_POSITION': (10, 10),
    'FUULSCREEN': False,
    'GRAB_MODE': 1,
    'SHOW_POINTER': False,
    'POINTER_COLOR': (0, 255, 0),
    'DRAW_POINTS': False,
    'CURSOR_TYPE': 'point',
    'ON_CONSOLE': False,
    }

cfg_settings = Config()
cfg_settings = load_config('cfg/default.cfg', cfg_settings)