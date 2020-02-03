import os.path, sys

def parsing(line, world, camera=None):
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
    elif line[:1] == '$':
        command = line[1:]
        if command[:10] == 'add-model ':
            resize = 1
            color_m = (0, 225, 225)
            position=[0,0,0]
            command_e = command.replace('add-model ', '')
            array = command_e.split(';')
            if os.path.exists('models/' + array[0] + '.obj'):
                if len(array) > 1:
                    arg_c = 1
                    while arg_c <= len(array)-1:
                        if str(array[arg_c]).replace(' ', '')[:2] == '-r':
                            resize = array[arg_c].replace('-r', '')
                            if resize.isdigit():
                                resize = int(resize)
                        elif str(array[arg_c]).replace(' ', '')[:2] == '-c':
                            color = array[arg_c].replace('-c', '').replace(' ', '').split(',')
                            color_rgb = []
                            for color_1 in color:    
                                if color_1.isdigit():
                                    color_1 = int(color_1)
                                    color_rgb.append(color_1)
                            if len(color_rgb) == 3:
                                color_m = color_rgb
                        elif str(array[arg_c]).replace(' ', '')[:2] == '-p':
                            position_a = array[arg_c].replace('-p', '').replace(' ', '').split(',')
                            position_l = []
                            for position_1 in position_a:    
                                if position_1.isdigit():
                                    position_1 = int(position_1)
                                    position_l.append(position_1)
                            if len(position_l) == 3:
                                position = position_l
                        arg_c += 1
                world.add_obj_model('models/' + array[0] + '.obj', resize=float(resize), color=color_m, position=position)
                print('Added')
            else:
                print('Invalid command[have no model]')
        elif command[:8] == 'cam-pos ':
            command_e = command.replace('cam-pos ', '')
            array = str(command_e).replace(' ', '').split(',')
            if len(array) == 3:
                if camera:
                    camera.pos = [int(array[0]),int(array[1]),int(array[2])]
                    print('Moved')
            else:
                print('Invalid command[to many args]')
        elif command[:10] == 'save_world':
            world.save_world()
        elif command[:11] == 'load_world ':
            command = command[11:].replace(' ', '')
            if os.path.exists(command):
                world.load_world(command)
        elif command[:5] == 'axes ':
            command = command[:5].replace(' ', '')
            world.add_axes(mode=command, color=(255, 0, 0))
                    
        elif command == 'exit':
            sys.exit()
        else:
            print('Invalid command[command not found]')
    return return_data