import os
import numpy as np

# class Test():
#     max_id = -1
#     origin = (0.0,0.0,0.0)

#     __init__(self, params,dir=None):
#         if dir is not None:
#             self.dir=dir
#         self.params = params

#         self.var_x = self.params['x_axis']['var']
#         self.var_y = self.params['y_axis']['var']

#         self.inc_x = self.params['x_axis']['increment']
#         self.inc_y = self.params['y_axis']['increment']

#         self.init_x = self.params[var_x]
#         self.init_y = self.params[var_y]

#         self.stride_x = self.params['stride_x']
#         self.stride_y = self.params['stride_y']
#         self.stride_z = self.params['stride_z']
#         self.layers = self.params['layers']
#         self.line_length = self.params['line_length']
#         self.pos = np.array(origin)

#     def generate_gcode(self):
#         lines = []
#         if self.params['scheme'] is 'line-grid-y':
#         count = 0

#         self.params[var_x] = init_x
#         for layer in range(self.layers):
#             layer = []
#             while pos[0] < bed_dims[0]-stride_x:
#                 column = []
#                 self.params[var_y] = init_y
#                 add_gcode_column(gcode_name, pos, power = self.params['laser_power_W'],
#                                                  feed = self.params['feed_rate_ipm'], 
#                                                  powder = self.params['powder_feed_rpm'])
#                 while pos[1] <bed_dims[1]-stride_y:
#                     point_1 = np.around(pos,4)
#                     pos[1]+=line_length
#                     point_2 = np.around(pos,4)
#                     pos[1] = point_1[1] + stride_y
#                     line = tuple((tuple(point_1),tuple(point_2)))
#                     add_gcode_line(gcode_name, line, power = self.params['laser_power_W'],
#                                                  feed = self.params['feed_rate_ipm'], 
#                                                  powder = self.params['powder_feed_rpm'])
                    
#                     column.append(line)
#                     self.params[var_y] += inc_y

#                 layer.append(column)
#                 self.params[var_x] += inc_x

#                 pos[0] += stride_x
#                 pos[1] = origin[0]
#             lines.append(layer) 
#             pos[2] += stride_z
#             pos[0] = origin[0]
#             pos[1] = origin[1]

#         return lines
    
    # def get_test_id(self):
    #     _files = []
    #     for (dir_path, dir_names, file_names) in os.walk(self.dir):
    #         _files+=(file_names)

    #     json_files = [file for file in _files if file.split('.')[-1]=='json']

        

    #     for f in json_files:
    #         id=int(f.split('.')[0].split('_')[-1])
    #         if id > max_id:
    #             max_id = id
        
    #     self.id=max_id+1

class Column():
    id = 0

    def __init__(self, start, stride = .5, length = 3, line_dict=None, var = None, inc = 0):
        self.pos = start
        self.stride = stride
        # self.line_dict = line_dict
        self.length = length
        self.lines = []
        self.id = Column.id
        Column.id+=1
        self.var = var
        self.inc = inc
        self.generate_lines(line_dict)
        
        
    def generate_lines(self,line_dict):
        while self.pos[1]< self.length - self.stride:
            self.lines.append(Line(self.pos,**line_dict))
            self.pos = self.pos+np.array((0,self.stride,0))
            print('stride+pos',self.pos[1] + self.stride)
            print('y:',self.pos[1])
            line_dict[self.var] += self.inc
            print(self.pos)

    def as_gcode(self):
        gcode = '(Column ' + str(self.id) + 'of stride' + str(self.stride) + ')\n'
        for line in self.lines:
            gcode += line.as_gcode()
    def as_dict(self):
        _dict = {'Column': self.id,
                'Stride': self.stride,
                'Lines': [line.as_dict() for line in self.lines],
                'Variable': self.var,
                'Increment': self.inc

        }
    def as_json(self):
        import json
        return json.dumps(self.as_dict())

class Line():

    id = 0

    def __init__(self, start, length=.25, power = 200, powder = 4, feed = 6):
        self.start = start
        self.length = length
        self.end = self.start + np.array((0,self.length,0))
        self.id = Line.id
        Line.id+=1
        self.power = power
        self.powder = powder
        self.feed = feed
    
    def as_gcode(self):
        gcode = '(Line ' + str(self.id) + 'of length' + str(self.length) + ')\n'
        gcode += 'M302 P' + str(self.powder) + '\n'
        gcode += 'G1 X'+str(self.start[0]) + ' Y' + str(self.start[1]) + ' Z' + str(self.start[2])+ ' F' + str(self.feed)
        gcode += '(Laser On)\n' + 'M3 S' + str(self.power)+'\n'
        gcode += 'G1 X'+str(self.end[0]) + ' Y' + str(self.end[1])+ ' Z' + str(self.end[2])
        gcode += '(Laser Off)\n' + 'M5' + '\n'
        return gcode

    def as_dict(self):

        _dict = { 'Line': self.id,
                'Length': self.length,
                'Power': self.power,
                'Feed': self.feed,
                'Powder':  self.powder,
                'Points:': {
                    'Start': {
                        'x':self.start[0].astype(float),
                        'y': self.start[1].astype(float),
                        'z': self.start[2].astype(float),
                    },
                    'End': {
                        'x':self.end[0].astype(float),
                        'y': self.end[1].astype(float),
                        'z': self.end[2].astype(float),
                    },
                },



        }
        return _dict

    def as_json(self):
        import json
        return json.dumps(self.as_dict())


if __name__ == '__main__':
    origin = np.array([0,0,0])
    column_dict = {'var':'power',
                    'inc':50,
                    'stride':.5,
                    'length':3,
                    'line_dict':{
                        'power':200,
                        'powder':3,
                        'feed':6,
                        'length':.25,
                        
                        },

                    }

    
    column = Column(origin,**column_dict)

    line_dict={
                        'power':200,
                        'powder':3,
                        'feed':6,
                        'length':.25,
                        
                        }

    line = Line(origin,**line_dict)

    with open('test.json','w') as f:
        f.write(column.as_json())