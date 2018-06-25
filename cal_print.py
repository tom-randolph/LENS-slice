
from lens_cal import Print

print_params = {
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