import tkinter as tk
root = tk.Tk()
CURSOR_TYPES                = {
    'point': 1,
    'axis': 2
}
SCREEN_RESOLUTION           = (800, 800)                                            #   Кастомное разрешение        
NATIVE_RESOLUTION           = (root.winfo_screenwidth(), root.winfo_screenheight()) #   Ваше разрешение             
SET_NATIVE_RESOLUTION       = True                                                  #   Использовать ваше разрешение
FPS_MAX	                    = 60                                                    #   Максимальный FPS             
FPS_POSITION                = (10, 10)                                              #   Место отображения FPS       
FUULSCREEN 	                = True                                                  #   Полно экранный режим         
GRAB_MODE                   = 1                                                     #   Захват курсора              
SHOW_POINTER                = True                                                  #   Показать центр(прицел)      
POINTER_COLOR               = (0, 255, 0)                                           #   Цвет прицела                
DRAW_POINTS                 = False                                                 #   Рисовать точки соеденения         
CURSOR_TYPE                 = 'point'                                               #   Тип прицела                 