from modules.obj_reader import get_model
import os, random
from shutil import copyfile
import colorama
from colorama import Fore, Back, Style
colorama.init()

def print_ok(string):
    print(Fore.GREEN + str(string) + Fore.WHITE)

class world:
    def __init__(self, name, color=(255, 255, 255)):
        self.name       = name
        self.blocks     = []

    def save_world(self):
        dir_create_nomber = 0
        while True:
            try:
                dir_create_plas = ''
                if dir_create_nomber !=0 : dir_create_plas = str(dir_create_nomber)
                dir_w = 'worlds/' + self.name + dir_create_plas
                os.mkdir(dir_w)
                break
            except:
                dir_create_nomber += 1
        with open(dir_w + '/data.wld', 'w', encoding="utf8") as f:
            for block in self.blocks:
                if block['model_dir']:
                    try:
                        os.mkdir(dir_w + '/models/')
                        # print(block['model_dir'])
                        # print(dir_w + '/' + block['model_dir'])
                        copyfile(block['model_dir'], dir_w + '/' + block['model_dir'])
                        f.write('model:dir:' + str(dir_w) + '/' + str(block['model_dir']) + '\\pos:' + str(block['pos'][0])
                            + '@' + str(block['pos'][1]) + '@' + str(block['pos'][2]) + '\\color:' 
                            + str(block['color'][0]) + '@' + str(block['color'][1]) + '@' + str(block['color'][2]) + '\\resize:' + str(block['resize']) + '\\id:' + str(block['id']) + '\n')

                    except:
                        pass

    def load_world(self, world_dir):
        with open(world_dir + '/data.wld', 'r', encoding="utf8") as f:
            for line in f.readlines():
                if line[:6] == 'model:':
                    data_load = {}
                    data = line[6:].replace('\n', '')
                    data_list = data.split('\\')
                    for argument in data_list:
                        if '@' in argument:
                            data_arg = argument.split(':')
                            data_load[data_arg[0]] = data_arg[1].split('@')
                        else:
                            data_arg = argument.split(':')
                            data_load[data_arg[0]] = data_arg[1]
                    model_points, connections = get_model(data_load['dir'], float(data_load['resize']))
                    data_load_in = {
                        'id': str(data_load['id']),
                        'name': str(data_load['dir']),
                        'model_dir': data_load['dir'],
                        'cube_points_dict': model_points,
                        'connections': connections,
                        'pos': [int(data_load['pos'][0]), int(data_load['pos'][1]), int(data_load['pos'][2])],
                        'color': (int(data_load['color'][0]), int(data_load['color'][1]), int(data_load['color'][2])),
                        'resize': float(data_load['resize'])
                    }
                    self.blocks.append(data_load_in)
                    print_ok("Added [dir='" + str(data_load['dir']) + "'; id=" + str(data_load['id']) + "]")

    def add_obj_model(self, filename, position={0, 0, 0}, color=(255, 255, 255), resize=None, id_model=None):
        model_points, connections = get_model(filename, resize)
        x = position[0]
        y = position[1]
        z = position[2]
        if not id_model:
            id_model_b = random.randint(0, 100)
            for block in self.blocks:
                if id_model_b == block.get('id'):
                    id_model_b = random.randint(0, 100)
                    break
            id_model = id_model_b
        else:
            id_model_b = id_model[:]
            for block in self.blocks:
                if id_model_b == block.get('id'):
                    id_model_b = id_model + str(random.randint(0, 100))
                    break
            id_model = id_model_b
        print_ok("Added [dir='" + str(filename) + "'; id=" + str(id_model) + "]")
        data = {
            'id': str(id_model),
            'name': str(filename),
            'model_dir': filename,
            'cube_points_dict': model_points,
            'connections': connections,
            'pos': [int(x), int(y), int(z)],
            'color': (int(color[0]), int(color[1]), int(color[2])),
            'resize': resize
        }
        self.blocks.append(data)


    def add_axes(self, color=(255, 255, 255), resize=None, mode='4', id_model=None):
        x = 0
        y = 0
        z = 0
        if mode == '3':
            cube_points_dict = [
                (0, 0, 0),
                (0, 0, 0),
                (0, 100, 0),
                (0, 0, 100),
            ]
        elif mode == '2':
            cube_points_dict = [
                (0, 0, 0),
                (100, 0, 0),
                (0, 0, 0),
                (0, 0, 100),
            ]
        elif mode == '1':
            cube_points_dict = [
                (0, 0, 0),
                (100, 0, 0),
                (0, 100, 0),
                (0, 0, 0),
            ]
        else:
            cube_points_dict = [
                (0, 0, 0),
                (100, 0, 0),
                (0, 100, 0),
                (0, 0, 100),
            ]

        connections = [(0, 1), (0, 2), (0, 3)]
        if not id_model:
            id_model_b = random.randint(0, 100)
            for block in self.blocks:
                if id_model_b == block.get('id'):
                    id_model_b = random.randint(0, 100)
                    break
            id_model = id_model_b
        else:
            id_model_b = id_model[:]
            for block in self.blocks:
                if id_model_b == block.get('id'):
                    id_model_b = id_model + str(random.randint(0, 100))
                    break
            id_model = id_model_b
        print_ok("Added [name='axes'; id=" + str(id_model) + "]")
        data = {
            'name': 'axes',
            'model_dir': None,
            'cube_points_dict': cube_points_dict,
            'connections': connections,
            'pos': [int(x), int(y), int(z)],
            'color': (int(color[0]), int(color[1]), int(color[2])),
            'resize': resize
        }

        self.blocks.append(data)
