import os.path, sys


def load_config(file, config, parsing, world, camera):
    if os.path.exists(file):
        with open(file, 'r') as f:
            for line in f.readlines():
                data = parsing(line, world, camera)
                if data and data[0] == 'SET':
                    if data[1][0] in config:
                        config[data[1][0]] = data[1][1]
    return config

def console(world, camera, config, parsing):
    manual = """HELP:
1. $add-model <model name>; -r <resize>; -c <color(r, g, b)>; -p <position(x, y, z)>
2. $cam-pos x, y, z
3. $cfg <config name(like: default)>
4. $save_world
5. $load_world <dir (like: worlds/Simple/)>
6. $axes <axes mode 1, 2, 3, 4>
7. SET <const> = <value>
8. cfg <config name>
"""
    print(manual)
    while True:
        resize = 1
        command = input('console> ')
        if command[:5] == '$cfg ':
            command_e = command.replace('$cfg ', '')
            if os.path.exists('cfg/' + command_e + '.cfg'):
                config = load_config('cfg/' + command_e + '.cfg', config, parsing, world, camera)
            else:
                print('Invalid command[cfg not found]')
        else:
            data = parsing(command, world, camera)
            if data and data[0] == 'SET':
                if data[1][0] in config:
                    config[data[1][0]] = data[1][1]
