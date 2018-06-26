import os
import numpy as np
import sys
from copy import deepcopy


'''This module is used to generate test prints for calibration. Units are in inches, ipm, Watts, and rpm. Instanciate
a Print object using a parameters dictionary (see bottom for example). Then write the files.'''

class Print():

    '''This class wraps all the logic to create gcode and json files for a print. The structure of the print is a series
    columns, creating a grid. Each column contains "lines", with are short depositions of material. The idea is that
    by traversing the grid, you can modify print parameters along the columns and rows, such that each line is unique. 
    The print paramaters you can modify are the powder feed rate, the print head feed rate, and the laser power.'''

    # Each print has a unique id, starting at 0. This is updated each time a Print object is instanciated (see update_id)
    id = -1

    # This is represents the print origin. np array for element wise operations
    origin = np.array((0,0,0))

    def __init__(self, layer_height = .01, layers = 10, layer_dict = None, dir = 'tests/'):

        '''All arguments are inteded to be passed in as a dictionary (see bottom for example)'''

        Print.update_id(dir)
        self.id = Print.id

        # The class variable is explicitly copied to avoid passing by reference and changing the origin
        self.pos = Print.origin.copy()
        self.layer_height = layer_height
        self.num_layers = layers
        self.layers = []
        self.generate_layers(deepcopy(layer_dict))
        self.dir = dir



    def generate_layers(self, _dict):
        '''This method generates each layer of the print, incrementing the Z position each time'''

        for _ in range(self.num_layers):
            self.layers.append(Layer(self.pos,**_dict))
            self.pos = self.pos+np.array((0, 0, self.layer_height))


    def as_gcode(self):
        ''' This method returns the string representation of the gcode for the print'''

        gcode = '(Print ' + str(self.id) + ')\n'
        for layer in self.layers:
            gcode += layer.as_gcode()
        return gcode

    def as_dict(self):
        ''' This method returns the dictionary representation of the data for the print'''

        _dict = {'Print': self.id,
                'Number of Layers': len(self.layers),
                'Layer Height': self.layer_height,
                'Layers': [layer.as_dict() for layer in self.layers],
        }
        return _dict

    def as_json(self):
        '''This method returns the string representation of the json, as translated from the dictionary'''
        import json
        return json.dumps(self.as_dict(), indent = 4)

    def update_id(dir):
        '''This method traverses the specified directory (default is "tests/") and finds the previous print files. 
        It updates the class variable "id" such that it does not overwrite old tests.'''
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
        
        '''Writes the gcode file in the specified directory (default is "test/")'''
        
        # Wrapped in try statement just to prevent creating empty files or directories in case of error 
        try:
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
        except:
            print('Could not write GCODE file')
            raise
        
    def write_json_file(self, dir = None):
         '''Writes the json file in the specified directory (default is "test/")'''
        
        # Wrapped in try statement just to prevent creating empty files or directories in case of error 
        try:
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
        except:
            print('Could not write JSON file')
            raise

    def write_files(self, dir = None):
        self.write_json_file(dir)
        self.write_gcode_file(dir)
        

class Layer():
    '''Reperesents the data associated with each layer of the print and is made up of "columns". As each columnn is generated, 
    a print variable is incremented accordingly. The space bewtween the *start* of each column is determined by the stride'''

    id = 0
    origin = np.array((0,0,0))

    def __init__(self, start = None, stride = .24, width = 3, column_dict = None, var = None, inc = 0):
        '''Variables are intended to be passed as a "layer_dict" by the parent "Print" object'''

        self.id = Layer.id
        Layer.id+=1
        if start is None:
            self.pos = Layer.origin.copy()
        else: self.pos = start
        self.stride = stride
        self.width = width
        self.columns = []
        self.var = var
        self.inc = inc

        # Deep copy is required to not overwrite the parent dictionary, which causes the column variable to not reset bewteen layers (bad!)
        self.generate_columns(deepcopy(column_dict))
    
    def generate_columns(self,_dict):
        '''Generates as many columns as will fit in the build volume, based on stride width'''

        while self.pos[0]< self.width - self.stride:
            self.columns.append(Column(self.pos,**_dict))

            # Increment the position in X
            self.pos = self.pos+np.array((self.stride, 0, 0))

            # Increment the variable by respective amount
            _dict['line_dict'][self.var] += self.inc

    def as_gcode(self):
        ''' This method returns the string representation of the gcode for the print'''

        gcode = '(Layer ' + str(self.id) + ' of stride ' + str(self.stride) + ')\n'
        for column in self.columns:
            
            if self.var is 'powder':
                gcode += '(Let Powder Spool Up)\n'
                gcode += 'M302 P' + str(column.lines[0].powder)
                gcode += ' (Dwelling 8 seconds)\n'
                gcode += 'G04 P' + str(45000) + '\n'
                
            gcode += 'G0 X' + str(column.lines[0].start[0]) + ' Y' + str(column.lines[0].start[1]) + ' Z' + str(column.lines[0].start[2]) + '\n'
            gcode += column.as_gcode()
        return gcode

    def as_dict(self):
        ''' This method returns the dictionary representation of the data for the print'''

        _dict = {'Layer': self.id,
                'Stride': self.stride,
                'Variable': self.var,
                'Increment': self.inc,
                'Columns': [column.as_dict() for column in self.columns],
                

        }
        return _dict

    def as_json(self):
        '''This method returns the string representation of the json, as translated from the dictionary'''

        import json
        return json.dumps(self.as_dict())
    
    
class Column():
    '''This class represents each individual column of the print grid. These columns are made up of lines. Each has a unique id. As each line is generated, 
    a print variable is incremented accordingly.The space bewtween the *start* of each line is determined by the stride'''

    id = 0

    def __init__(self, start, stride = .5, length = 3, line_dict=None, var = None, inc = 0):
        '''The variables of this will be passed in from the parent layer as a dictionary'''

        self.pos = start
        self.stride = stride
        self.length = length
        self.lines = []
        self.id = Column.id
        Column.id+=1
        self.var = var
        self.inc = inc

        # Deep copy is required to not overwrite the parent dictionary, which causes the column variable to not reset bewteen layers (bad!)
        self.generate_lines(deepcopy(line_dict))
        
        
    def generate_lines(self,_dict):
        '''Generates as many lines as will fit in the build volume, based on stride length'''
        while self.pos[1]< self.length - self.stride:
            self.lines.append(Line(self.pos,**_dict))

            # Increment the position in the Y
            self.pos = self.pos+np.array((0,self.stride,0))

            #Increment the variable by the respective amount
            _dict[self.var] += self.inc




    def as_gcode(self):
        ''' This method returns the string representation of the gcode for the column'''

        gcode = '(Column ' + str(self.id) + ' of stride ' + str(self.stride) + ')\n'
        for line in self.lines:
            if self.var is 'powder':
                gcode += '(Let Powder Spool Up)\n'
                gcode += 'M302 P' + str(line.powder) + '\n'
                gcode += 'G4 P8000\n'
            gcode += line.as_gcode()
        return gcode

    def as_dict(self):
       ''' This method returns the dictionary representation of the data for the column'''

        _dict = {
                'Column': self.id,
                'Stride': self.stride,
                'Lines': [line.as_dict() for line in self.lines],
                'Variable': self.var,
                'Increment': self.inc

        }
        return _dict

    def as_json(self):
        '''This method returns the string representation of the json, as translated from the dictionary'''

        import json
        return json.dumps(self.as_dict())

class Line():
    '''This class represents each individual line int the print. Each has a unique id.'''

    id = 0

    def __init__(self, start, length=.25, power = 200, powder = 4, feed = 6):
        '''The variables of this will be passed in from the parent column as a dictionary'''

        self.id = Line.id
        Line.id+=1

        # np around is used to trunctate the trailing digits in case of imperfect FP representations (common). 2 decimal places are used
        self.start = np.around(start,2)
        self.length = length
        self.end = np.around(start + np.array((0,self.length,0)),2)
        self.power = np.around(power, 2)
        self.powder = np.around(powder, 2)
        self.feed = np.around(feed, 2)
    
    def as_gcode(self):
        ''' This method returns the string representation of the gcode for the line. Feed rates and laser powers are expressed explicitly for clarity'''

        gcode = '(Line ' + str(self.id) + ' of length ' + str(self.length) + ')\n'
        gcode += 'G1 X'+str(self.start[0]) + ' Y' + str(self.start[1]) + ' Z' + str(self.start[2])+ ' F' + str(self.feed) + '\n'
        gcode += '(Laser On)\n' + 'M3 S' + str(self.power)+'\n'
        gcode += 'G1 X'+str(self.end[0]) + ' Y' + str(self.end[1])+ ' Z' + str(self.end[2]) + '\n'
        gcode += '(Laser Off)\n' + 'M5' + '\n'
        return gcode

    def as_dict(self):
        ''' This method returns the dictionary representation of the data for the line.'''

        # Many of these are of type np.float64, and must be cast to primitve types to be translated to json later (astype(float))
        _dict = { 'Line': self.id,
                'Length': self.length,
                'Power': self.power.astype(float),
                'Feed': self.feed.astype(float),
                'Powder':  self.powder.astype(float),
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
        '''This method returns the string representation of the json, as translated from the dictionary'''
        
        import json
        return json.dumps(self.as_dict())


if __name__ == '__main__':

    print_params = {
    'dir': 'dev',
    'layer_height': .01,
    'layers': 5,
    'layer_dict': 
        {
        'var':'powder',
        'inc': .5,
        'stride': .25,
        'column_dict' : 
            {
            'var':'power',
            'inc':50,
            'stride':.5,
            'line_dict':
                {
                'power':100,
                'powder':2,
                'feed':15,
                'length':.25,
                        
                },

            },
        },
    }


test_1 = Print(**print_params)

test_1.write_files()

    
    