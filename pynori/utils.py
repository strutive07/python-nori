
import csv
import pickle
import time
from functools import wraps
from datetime import datetime


def save_pkl(data, name):   # name: ‘..._pkl'
    fp = open(name, 'wb')
    pickle.dump(data, fp)
    fp.close()
    
def load_pkl(name):         # name: ‘..._pkl'
    fp = open(name, 'rb')
    return pickle.load(fp)

def load_lines(data_path):
    data_list = []
    with open(data_path, 'r', encoding='utf-8') as rf:
        for line in rf:
            line = line.strip()
            data_list.append(line)
    return data_list

def smart_split(in_str):
    # input:   '"aaaa",32,"bbbb","ccc,ddd"'
    # output:  ['aaaa', '32', 'bbbb', 'ccc,ddd']
    splited_arr = ['{}'.format(x) for x in list(csv.reader([in_str], delimiter=',', quotechar='"'))[0]]
    return splited_arr

def calc_execution_time(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        print(end - start)
        return result
    return inner