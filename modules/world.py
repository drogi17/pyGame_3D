from modules.obj_reader import get_model
import os
from shutil import copyfile

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
        with open(dir_w + '/data.wld', 'w') as f:
            for block in self.blocks:
                if block['model_dir']:
                    try:
                        os.mkdir(dir_w + '/models/')
                        # print(block['model_dir'])
                        # print(dir_w + '/' + block['model_dir'])
                        copyfile(block['model_dir'], dir_w + '/' + block['model_dir'])
                        f.write('model:dir:' + str(dir_w) + '/' + str(block['model_dir']) + '\\pos:' + str(block['pos'][0])
                            + '@' + str(block['pos'][1]) + '@' + str(block['pos'][2]) + '\\color:' 
                            + str(block['color'][0]) + '@' + str(block['color'][1]) + '@' + str(block['color'][2]) + '\\resize:' + str(block['resize']) + '\n')

                    except:
                        pass

    def load_world(self, world_dir):
        with open(world_dir + '/data.wld', 'r') as f:
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
                        'model_dir': data_load['dir'],
                        'cube_points_dict': model_points,
                        'connections': connections,
                        'pos': [int(data_load['pos'][0]), int(data_load['pos'][1]), int(data_load['pos'][2])],
                        'color': (int(data_load['color'][0]), int(data_load['color'][1]), int(data_load['color'][2])),
                        'resize': float(data_load['resize'])
                    }
                    self.blocks.append(data_load_in)

    def add_obj_model(self, filename, data={'x':0, 'y':0, 'z':0}, color=(255, 255, 255), resize=None):
        model_points, connections = get_model(filename, resize)
        x = data['x']
        y = data['y']
        z = data['z']
        data = {
            'model_dir': filename,
            'cube_points_dict': model_points,
            'connections': connections,
            'pos': [int(x), int(y), int(z)],
            'color': (int(color[0]), int(color[1]), int(color[2])),
            'resize': resize
        }
        self.blocks.append(data)


    def add_axes(self, color=(255, 255, 255), resize=None):
        x = 0
        y = 0
        z = 0
        cube_points_dict = [
            (0, 0, 0),
            (100, 0, 0),
            (0, 100, 0),
            (0, 0, 100),
        ]

        connections = [(0, 1), (0, 2), (0, 3)]

        data = {
            'model_dir': None,
            'cube_points_dict': cube_points_dict,
            'connections': connections,
            'pos': [int(x), int(y), int(z)],
            'color': (int(color[0]), int(color[1]), int(color[2])),
            'resize': resize
        }

        self.blocks.append(data)
