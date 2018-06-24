import os
import numpy as np
import sys


class Print():

    id = -1
    origin = np.array((0,0,0))

    def __init__(self, layer_height = .01, layers = 10, layer_dict = None, dir = 'tests/'):
        Print.update_id(dir)
        self.id = Print.id
        self.pos = Print.origin.copy()
        self.layer_height = layer_height
        self.num_layers = layers
        self.layers = []
        self.layer_dict = layer_dict
        self.generate_layers(layer_dict.copy())
        self.dir = dir



    def generate_layers(self, layer_dict):

        for _ in range(self.num_layers):
            self.layers.append(Layer(self.pos,**layer_dict))
            self.pos = self.pos+np.array((0, 0, self.layer_height))


    def as_gcode(self):
        gcode = '(Print ' + str(self.id) + ')\n'
        for layer in self.layers:
            gcode += layer.as_gcode()
        return gcode

    def as_dict(self):
        _dict = {'Print': self.id,
                'Number of Layers': len(self.layers),
                'Layer Height': self.layer_height,
                'Layers': [layer.as_dict() for layer in self.layers],
        }
        return _dict

    def as_json(self):
        import json
        return json.dumps(self.as_dict())

    def update_id(dir):
        _files = []
        for (dir_path, dir_names, file_names) in os.walk(dir):
            _files+=(file_names)

        json_files = [file for file in _files if file.split('.')[-1]=='json']
        max_id = 0
        for f in json_files:
            id=int(f.split('.')[0].split('_')[-1])
            if id > max_id:
                max_id = id

        Print.id=max_id+1
    
    def write_gcode_file(self, dir = None):
        
        if dir is None:
            dir = self.dir

        if not os.path.exists(dir):
            os.mkdir(dir)

        self.gcode_file = os.path.join(dir, 'test_' + str(self.id) + '.gcode')
        if os.path.isfile(self.gcode_file):
            print('A gcode file for this test number already exists...')
            ans = input('Would you like to overwrite it? (y/n)')
            if ans in 'Yesyes':
                pass
            else: 
                print('No edits will be made. Specify output filename if desired.')
                sys.exit(1)
        with open(self.gcode_file, 'w')  as f:
            f.write("""G17 (XY Plane Select)
G20 (Use Inch Units, G21 is to use mm units)
G40 (Turn off cutter radius compensation)
G80 (Cancel canned cycles)
G90 (Use absolute distance mode.  G91 is to use relative distance mode)
G94 (Set feed rate - needs to have an "F" word after it)
G49 (Do NOT use tool length offset)
""")
            f.write(self.as_gcode())
        
    def write_json_file(self, dir = None):
        if dir is None:
            dir = self.dir

        if not os.path.exists(dir):
            os.mkdir(dir)

        self.json_file = os.path.join(dir, 'test_' + str(self.id) + '.json')
        if os.path.isfile(self.json_file):
            print('A json file for this test number already exists...')
            ans = input('Would you like to overwrite it? (y/n)')
            if ans in 'Yesyes':
                pass
            else: 
                print('No edits will be made. Specify output filename if desired.')
                sys.exit(1)
        with open(self.json_file, 'w') as f:
            f.write(self.as_json())
    def write_files(self, dir = None):
        self.write_json_file(dir)
        self.write_gcode_file(dir)
        


class Layer():

    id = 0
    origin = np.array((0,0,0))

    def __init__(self, start = None, stride = .24, width = 3, column_dict = None, var = None, inc = 0):
        if start is None:
            self.pos = Layer.origin.copy()
        else: self.pos = start
        self.stride = stride
        self.width = width
        self.columns = []
        self.column_dict = column_dict
        self.var = var
        self.inc = inc
        self.generate_columns(column_dict.copy())
    
    def generate_columns(self,column_dict):
        while self.pos[0]< self.width - self.stride:
            self.columns.append(Column(self.pos,**column_dict))
            self.pos = self.pos+np.array((self.stride, 0, 0))
            column_dict['line_dict'][self.var] += self.inc

    def as_gcode(self):
        gcode = '(Layer ' + str(self.id) + ' of stride ' + str(self.stride) + ')\n'
        for column in self.columns:
            gcode += column.as_gcode()
        return gcode

    def as_dict(self):
        _dict = {'Layer': self.id,
                'Stride': self.stride,
                'Columns': [column.as_dict() for column in self.columns],
                'Variable': self.var,
                'Increment': self.inc

        }
        return _dict

    def as_json(self):
        import json
        return json.dumps(self.as_dict())
    
    
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
        self.generate_lines(line_dict.copy())
        
        
    def generate_lines(self,line_dict):
        while self.pos[1]< self.length - self.stride:
            self.lines.append(Line(self.pos,**line_dict))
            self.pos = self.pos+np.array((0,self.stride,0))
            line_dict[self.var] += self.inc




    def as_gcode(self):
        gcode = '(Column ' + str(self.id) + ' of stride ' + str(self.stride) + ')\n'
        for line in self.lines:
            gcode += line.as_gcode()
        return gcode
    def as_dict(self):
        _dict = {'Column': self.id,
                'Stride': self.stride,
                'Lines': [line.as_dict() for line in self.lines],
                'Variable': self.var,
                'Increment': self.inc

        }
        return _dict
    def as_json(self):
        import json
        return json.dumps(self.as_dict())

class Line():

    id = 0

    def __init__(self, start, length=.25, power = 200, powder = 4, feed = 6):
        self.start = np.around(start,2)
        self.length = length
        self.end = np.around(start + np.array((0,self.length,0)),2)
        self.id = Line.id
        Line.id+=1
        self.power = power
        self.powder = powder
        self.feed = feed
    
    def as_gcode(self):
        gcode = '(Line ' + str(self.id) + ' of length ' + str(self.length) + ')\n'
        gcode += 'M302 P' + str(self.powder) + '\n'
        gcode += 'G1 X'+str(self.start[0]) + ' Y' + str(self.start[1]) + ' Z' + str(self.start[2])+ ' F' + str(self.feed) + '\n'
        gcode += '(Laser On)\n' + 'M3 S' + str(self.power)+'\n'
        gcode += 'G1 X'+str(self.end[0]) + ' Y' + str(self.end[1])+ ' Z' + str(self.end[2]) + '\n'
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

    print_params = {
    'layer_height': .01,
    'layers': 10,
    'layer_dict': 
        {
        'var':'powder',
        'inc': .6,
        'stride': .7,
        'width' : 3.4,
        'column_dict' : 
            {
            'var':'power',
            'inc':100,
            'stride':.6,
            'length':3.2,
            'line_dict':
                {
                'power':220,
                'powder':3.3,
                'feed':2.2,
                'length':.22,
                        
                },

            },
        },
    }


    print_one = Print(**print_params)
    # print(print_one.layers)
    print_one.write_files()
    
    