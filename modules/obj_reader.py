def get_model(file, resize):
    points  = []
    connects_dict = []
    with open(file, 'r') as f:
        for line in f.readlines():
            if line[0] == 'v' and line[1] == ' ':
                line = line.replace('v ', '').replace('\n', '')
                cords = line.split(' ')
                corda_float = []
                for cord in cords:
                    if resize:
                        if cord != '':
                            corda_float.append(float(cord)*resize)
                    else:
                        if cord != '':
                            corda_float.append(float(cord))
                if len(corda_float) > 0:
                    points.append(corda_float)
            elif line[0] == 'f':
                line = line.replace('f ', '').replace('\n', '')
                connects = line.split(' ')
                list_cord = []
                for connect in connects:
                    conn_cords = connect.split('/')[0]
                    if conn_cords != '':
                        list_cord.append(int(conn_cords)-1)
                connects_dict.append(list_cord)
    return points, connects_dict