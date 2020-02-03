import os.path

def load_config(file, cfg_settings):
    with open(file, 'r') as f:
        for line in f.readlines():
            coments = line.find('#')
            if coments != -1:
                line = line[:coments]
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
                if setting[0] in cfg_settings:
                    cfg_settings[setting[0]] = setting[1]
    return cfg_settings

def console(world, camera, config):
    manual = """HELP:
1. add-model <model name> -r <resize>
2. cam-pos x, y, z
3. add-const <Const_name>=<value>
4. cfg <config name(like: default)>
"""
    print(manual)
    while True:
        resize = 1
        command = input('console> ')
        if command[:10] == 'add-model ':
            command_e = command.replace('add-model ', '')
            array = command_e.split(' ')
            if os.path.exists('models/' + array[0] + '.obj'):
                if len(array) > 1:
                    if array[1][:3] == '-r ':
                        resize = array[1].replace('-r ', '')
                        if resize.isdigit():
                            resize = int(resize)
                world.add_obj_model('models/' + array[0] + '.obj', resize=resize, color=(0, 225, 225))
                print('Added')
            else:
                print('Invalid command[have no model]')
        elif command[:8] == 'cam-pos ':
            command_e = command.replace('cam-pos ', '')
            array = str(command_e).replace(' ', '').split(',')
            if len(array) == 3:
                camera.pos = [int(array[0]),int(array[1]),int(array[2])]
                print('Moved')
            else:
                print('Invalid command[to many args]')
        elif command[:10] == 'add-const ':
            command_e = command.replace('add-const ', '')
            array = str(command_e).replace(' ', '').split(';')
            for const in array:
                const_arr = const.split('=')
                print(const_arr)
                if const_arr[0] in config:
                    if const_arr[1] == 'False':
                        const_arr[1] = False
                    elif const_arr[1] == 'True':
                        const_arr[1] = True
                    elif str(const_arr[1]).isdigit():
                        const_arr[1] = int(const_arr[1])
                    elif ',' in const_arr[1]:
                        array = str(const_arr[1]).split(',')
                        nomb = 0
                        while nomb <= len(array)-1:
                            if str(array[nomb]).isdigit():
                                array[nomb] = int(array[nomb])
                            nomb += 1
                        const_arr[1] = array
                    config[const_arr[0]] = const_arr[1]
                    print('Changed')
                else:
                    print('Invalid command[invalid args]')
                    break
        elif command[:4] == 'cfg ':
            command_e = command.replace('cfg ', '')
            if os.path.exists('cfg/' + command_e + '.cfg'):
                config = load_config('cfg/' + command_e + '.cfg', config)
            else:
                print('Invalid command[cfg not found]')

        else:
            print('Invalid command[command not found]')
