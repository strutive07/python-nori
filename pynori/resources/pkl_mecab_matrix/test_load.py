

import pickle
import gzip
from datetime import datetime


def read_pkl(name):
    """ name: '~.pkl' """
    fp = open(name, 'rb')
    return pickle.load(fp)



start_main = datetime.now()


# load and uncompress.
#with gzip.open('matrix_def.pkl','rb') as rf:
#    data = pickle.load(rf)
# RUN TIME: 0:00:01.379878




data = read_pkl('matrix_def_p.pkl')
# RUN TIME: 0:00:01.103657



end_main = datetime.now()
print('\n RUN TIME: {}\n'.format(end_main - start_main))