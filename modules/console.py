import os.path, sys


def load_config(file, config, parsing, world, camera):
    if os.path.exists(file):
        with open(file, 'r', encoding="utf8") as f:
            nomber = 0
            for line in f.readlines():
                data = parsing(line, world, nomber, camera)
                if data and data[0] == 'SET':
                    if data[1][0] in config:
                        config[data[1][0]] = data[1][1]
                nomber += 1
    return config

def console(world, camera, config, parsing):
    manual = """HELP:
1. $add_model <model name>; -r <resize>; -c <color(r, g, b)>; -p <position(x, y, z)>; -i <id>
2. $move_camera x, y, z
3  $move_block <id>; x, y, z
4. $cfg <config name(like: default)>
5. $save_world
6. $load_world <dir (like: worlds/Simple/)>
7. $axes <axes mode 1, 2, 3, 4>
8. SET <const> = <value>
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
            nomber = 0
            data = parsing(command, world, nomber, camera)
            if data and data[0] == 'SET':
                if data[1][0] in config:
                    config[data[1][0]] = data[1][1]