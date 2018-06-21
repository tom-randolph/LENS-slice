'''This module controls printing calibration patterns for dimensional analysis'''
import json
import argparse
import os
import numpy as np


print_params = {
    
    'powder_feed_rpm': 3,
    'laser_power_W':200,
    'feed_rate_ipm':6,
    'scheme': 'line-grid-y',
    'x_axis': { 'var':'powder_feed_rpm', 'increment': .25},
    'y_axis': { 'var':'laser_power_W', 'increment': 50},
    'line_length': .25,
    'stride_x': .25,
    'stride_y': .5,
    'stride_z':.01,
    'layers': 10,
    
}

bed_dims = (3.0,3.0)


def get_test_id(json_dir):
    _files = []
    for (dir_path, dir_names, file_names) in os.walk(json_dir):
        _files+=(file_names)

    json_files = [file for file in _files if file.split('.')[-1]=='json']

    max_id = -1

    for f in json_files:
        id=int(f.split('.')[0].split('_')[-1])
        if id > max_id:
            max_id = id
    
    id=max_id+1
    return id


def add_gcode_column(file, pos,power = None,feed = None, powder = None):
    dwell = 8000
    factor = .182
    # dwell=np.around(dwell/factor,5)
    with open(file, 'a') as f:
        if powder is not None:
            # f.write('M302 P' + str(powder) + '\n')
            pass
        f.write('G0 X' + str(pos[0]) + ' Y' + str(pos[1]) + '\n')
        f.write('G4 P' + str(dwell) + '\n')


def add_gcode_line(file, line, power=None,feed=None, powder = None):
    '''appends the file with the code for the next drawn line'''

    point_1 = line[0]
    point_2 = line[1]


    gcode_move_1 = 'G1 X'+str(point_1[0]) + ' Y' + str(point_1[1])
    gcode_move_2 = 'G1 X'+str(point_2[0]) + ' Y' + str(point_2[1])
    if feed is not None:
        gcode_move_2+= ' F' + str(feed)
    
    
    with open(file, 'a') as f:

        # Comments the GCODE file for traceability

        f.write('(New Line)\n')
       

        f.write(gcode_move_1 + '\n')

        if power is not None:
            f.write('(Laser On)\n')
            f.write('M3 S' + str(power)+'\n')

        else: f.write('M3\n')
        f.write(gcode_move_2 + '\n')
        f.write('M5\n')
        f.write('(Laser Off)\n')


if __name__ == '__main__':

    gcode_name = 'test_1.txt'

    with open(gcode_name,'w') as f:
        f.write("""G17 (XY Plane Select)
G20 (Use Inch Units, G21 is to use mm units)
G40 (Turn off cutter radius compensation)
G80 (Cancel canned cycles)
G90 (Use absolute distance mode.  G91 is to use relative distance mode)
G94 (Set feed rate - needs to have an "F" word after it)
G49 (Do NOT use tool length offset)
""")

    origin = (0.0,0.0,0.0)

    

    var_x = print_params['x_axis']['var']
    var_y = print_params['y_axis']['var']

    inc_x = print_params['x_axis']['increment']
    inc_y = print_params['y_axis']['increment']

    init_x = print_params[var_x]
    init_y = print_params[var_y]

    stride_x = print_params['stride_x']
    stride_y = print_params['stride_y']
    stride_z = print_params['stride_z']
    layers = print_params['layers']
    line_length = print_params['line_length']

    lines = []
    if print_params['scheme'] is 'line-grid-y':
        count = 0
        pos = np.array(origin)
        print_params[var_x] = init_x
        for layer in range(layers):
            layer = []
            while pos[0] < bed_dims[0]-stride_x:
                column = []
                print_params[var_y] = init_y
                add_gcode_column(gcode_name, pos, power = print_params['laser_power_W'],
                                                 feed = print_params['feed_rate_ipm'], 
                                                 powder = print_params['powder_feed_rpm'])
                while pos[1] <bed_dims[1]-stride_y:
                    point_1 = np.around(pos,4)
                    pos[1]+=line_length
                    point_2 = np.around(pos,4)
                    pos[1] = point_1[1] + stride_y
                    line = tuple((tuple(point_1),tuple(point_2)))
                    add_gcode_line(gcode_name, line, power = print_params['laser_power_W'],
                                                 feed = print_params['feed_rate_ipm'], 
                                                 powder = print_params['powder_feed_rpm'])
                    
                    

                    column.append(line)
                    print_params[var_y] += inc_y

                layer.append(column)
                print_params[var_x] += inc_x

                pos[0] += stride_x
                pos[1] = origin[0]
            lines.append(layer) 
            pos[2] += stride_z
            pos[0] = origin[0]
            pos[1] = origin[1]

    
    
    json_dir = 'json/'
    
    id=get_test_id(json_dir)

    print('ID:',id)



    # with open(os.path.join(json_dir,'test_'+str(id))+'.json','w') as f:

    #     f.write(json.dumps(print_params))

    # print('JSON file created')
















































# def print_id(id):

#     numeral_dict={
#         1:'i'
#         2:'ii'
#         3:'iii'
#         4:'iv'
#         5:'v'
#         6:'vi'
#         7:'vii'
#         8: 'viii'
#         9: 'ix'
#         10:'x'
#         11:'xi'
#         12: 'xii'
#         13: 'xiii'
#         14: 'xiv',
#         15: 'xv',
#         16: 'xvi'
#         17:'xvii',
#         18: 'xviii'
#         19: 
#     }