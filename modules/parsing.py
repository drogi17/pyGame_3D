import os.path, sys
import copy
import colorama
from colorama import Fore, Back, Style
colorama.init()


def get_parametrs(string):
    parametr = []
    string = string.replace(' ', '')
    parametr.append(str(string)[:2])
    string = string[2:]
    parametr.append(string)
    return parametr

def print_ok(string):
    print(Fore.GREEN + str(string) + Fore.WHITE)

def print_error(string):
    print(Fore.RED + str(string) + Fore.WHITE)

class Handler:
    def __init__(self, argument, world, camera):
        self.argument = argument
        self.world    = world
        self.camera   = camera
        self.HANDLERS = {
           "move_camera": self.handle_cam_pos,
           "move_block": self.handle_move_block,
           "save_world": self.handle_save_world,
           "load_world": self.handle_load_world,
           "axes": self.handle_axes,
           "add_model": self.handle_add_model,
           "exit": sys.exit,
            }
    def handle_move_block(self):
        id_pos = str(self.argument).replace(' ', '').split(';')
        moved = False
        if len(id_pos) == 2:
            id_model, pos_model = id_pos
            print(id_model)
            print(pos_model)
            for block in self.world.blocks:
                block_id = block.get('id')
                print(block_id)
                print(id_model)
                if block_id == id_model:
                    array = str(pos_model).split(',')
                    block['pos'] = [int(array[0]),int(array[1]),int(array[2])]
                    print_ok('Camera moved => ' + str(block['pos']))
                    moved = True
                    break
        if not moved:
            print_error('Invalid command[not moded]')
        return self.world, self.camera

    def handle_cam_pos(self):
        array = str(self.argument).replace(' ', '').split(',')
        if len(array) == 3:
            if self.camera:
                self.camera.pos = [int(array[0]),int(array[1]),int(array[2])]
                print_ok('Camera moved => ' + str(self.camera.pos))
        else:
            print_error('Invalid command[to many args]')
        return self.world, self.camera

    def handle_save_world(self):
        self.world.save_world()
        print('World saved')
        return self.world, self.camera

    def handle_load_world(self):
        if os.path.exists(str(self.argument).replace(' ', '')):
            self.argument = self.argument.replace(' ', '')
            self.world.load_world(self.argument)
            print_ok('World loaded')
        else:
            print_error('World not loaded')
        return self.world, self.camera

    def handle_axes(self):
        self.world.add_axes(mode=self.argument, color=(255, 0, 0))
        return self.world, self.camera
    def handle_add_model(self):
        resize = 1
        color_m = (0, 225, 225)
        position = [0,0,0]
        id_model = None
        array = self.argument.split(';')
        if os.path.exists('models/' + array[0] + '.obj'):
            if len(array) > 1:
                arg_c = 1
                while arg_c <= len(array)-1:
                    parametr = get_parametrs(array[arg_c])
                    if parametr[0] == '-r':
                        try:
                            if parametr[1]:
                                resize = float(parametr[1])
                        except:
                            pass
                    elif parametr[0] == '-c':
                        color = parametr[1].split(',')
                        color_rgb = []
                        for color_1 in color:    
                            if color_1.isdigit():
                                color_1 = int(color_1)
                                color_rgb.append(color_1)
                        if len(color_rgb) == 3:
                            color_m = color_rgb
                    elif parametr[0] == '-p':
                        position_a = parametr[1].split(',')
                        position_l = []
                        for position_1 in position_a:    
                            if position_1.isdigit():
                                position_1 = int(position_1)
                                position_l.append(position_1)
                        if len(position_l) == 3:
                            position = position_l

                    elif parametr[0] == '-i':
                        id_model = parametr[1]
                    arg_c += 1
            self.world.add_obj_model('models/' + str(array[0]) + '.obj', resize=float(resize), color=color_m, position=position, id_model=id_model)
            # print_ok('Added [' + str(array[0]) + "]")
        else:
            print_error('Invalid command[have no model]')
        return self.world, self.camera

def parsing(line, world, nomber=0, camera=None):
    return_data = []
    coments = line.find('#')
    if coments != -1:
        line = line[:coments]
    line = str(line).replace('\n', '')
    if line[:5] == 'echo ':
        line = line[5:]
        print(line)
    elif line[:4] == 'SET ':
        setting = str(line).replace('SET ', '').replace(' ', '').replace('  ', '').split('=')
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
        return_data = ['SET', setting]
        print(str(setting[0]) + '=' + str(setting[1]))
    elif line[:1] == '$':
        command = line[1:]
        args_all = command.split(" ", 1)
        if len(args_all) >= 2:
            name, args = args_all
        else:
            name = args_all[0]
            args = None
        handlers = Handler(args, world, camera)
        handler = handlers.HANDLERS.get(name)
        if handler:
            world, camera = handler()
        else:
           print_error("[" + str(nomber+1) + "]Invalid command")
    elif line != '':
        print_error("[" + str(nomber+1) + "]Invalid command")
    return return_data