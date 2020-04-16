
import os
import sys
import pickle
import gzip
from datetime import datetime

#print(os.getcwd())
#print(sys.path[0])

cur_path = __file__
cur_path = '/'.join(cur_path.split('/')[:-2]) # ../resources/
#print(cur_path)

#parent_dir = os.path.dirname(sys.path[0])
#parent_dir = os.path.dirname(os.getcwd())
mecab_ko_dic_ver = 'mecab-ko-dic-2.1.1-20180720'

## pickle load & save
def write_pkl(data, name):
    """ name: '~.pkl' """ 
    fp = open(name, 'wb')
    pickle.dump(data, fp)
    fp.close()
def read_pkl(name):
    """ name: '~.pkl' """
    fp = open(name, 'rb')
    return pickle.load(fp)


# --------------------------------------------------------------------------------

start_main = datetime.now()


matrix_def_dict = dict()

with open(cur_path + '/' + mecab_ko_dic_ver + '/matrix.def', 'r') as rf:
    i = 0
    for line in rf:
        if i == 0:
            i += 1
            continue

        splited_line = line.strip().split()

        rightId = int(splited_line[0])
        leftId = int(splited_line[1])
        cost = int(splited_line[2])

        if matrix_def_dict.get(rightId) is None:
            matrix_def_dict[rightId] = dict()

        if matrix_def_dict[rightId].get(leftId) is None:
            matrix_def_dict[rightId][leftId] = dict()

        matrix_def_dict[rightId][leftId] = cost


        #if i == 3000:
        #    print(matrix_def_dict)
        #    break

        #i += 1


#write_pkl(matrix_def_dict, 'matrix_def_p.pkl')

# save and compress.
output_f_nm = 'matrix_def.pkl'
with gzip.open(cur_path + '/pkl_mecab_matrix/' + output_f_nm, 'wb') as wf:
    pickle.dump(matrix_def_dict, wf)


end_main = datetime.now()
print('> {} is successfully generated! - {}'.format(output_f_nm, end_main - start_main))


