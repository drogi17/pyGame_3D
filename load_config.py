import tkinter as tk
import os, sys
root = tk.Tk()
CURSOR_TYPES   = {
    'point': 1,
    'axis': 2
}



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
