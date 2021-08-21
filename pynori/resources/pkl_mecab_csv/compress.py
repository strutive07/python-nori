
import os
import sys
import shlex
import pickle
import gzip
from datetime import datetime

cur_path = __file__
back_1_path = '/'.join(cur_path.split('/')[:-2]) # ../resources/
back_2_path = '/'.join(back_1_path.split('/')[:-1]) # ../pynori/

mecab_ko_dic_ver = 'mecab-ko-dic-2.1.1-20180720'

sys.path.insert(0, back_2_path)
from pos import POS
#sys.path.insert(0, back_2_path + '/dict')
#from token_info_ds import DSManager
#from dictionary import Dictionary


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

total_entries = []
for dirName, subdirList, fileList in os.walk(back_1_path + '/' + mecab_ko_dic_ver):
    for fname in fileList:
        if fname.split('.')[-1] == 'csv':
            PATH_EACH = dirName + '/' + fname
            total_entries += open(PATH_EACH, 'r', encoding='UTF8').readlines()

#sysTokenInfo = Trie()
#print(len(total_entries))

refined_data = []

for entry in total_entries:
    entry = entry.strip()

    # Use shlex. 
    # to deal with the case: ",",1792,3558,788,SC,*,*,*,*,*,*,*
    shlex_splitter = shlex.shlex(entry, posix=True)
    shlex_splitter.whitespace = ','
    shlex_splitter.whitespace_split = True
    splits = list(shlex_splitter)
    #splits = entry.split(',')
    
    token = splits[0]
    
    morph_inf = dict()
    morph_inf['surface'] = splits[0]
    morph_inf['left_id'] = splits[1]
    morph_inf['right_id'] = splits[2]
    morph_inf['word_cost'] = int(splits[3])
    morph_inf['POS'] = splits[4]

    if splits[8] == '*': # 단일어
        morph_inf['POS_type'] = POS.Type.MORPHEME
        morph_inf['morphemes'] = None

    else: # 복합어

        mecab_pos_type_naming = splits[8].upper()
        if mecab_pos_type_naming == 'COMPOUND':
            morph_inf['POS_type'] = POS.Type.COMPOUND
        elif mecab_pos_type_naming == 'INFLECT':
            morph_inf['POS_type'] = POS.Type.INFLECT
        elif mecab_pos_type_naming == 'PREANALYSIS':
            morph_inf['POS_type'] = POS.Type.PREANALYSIS
        else:
            morph_inf['POS_type'] = mecab_pos_type_naming
        
        if len(splits[11].split('+')) == 1: # Compound인데 1개면 잘못 명시한 케이스 (확인 필요. 오류?)
            # 예외처리 (ex. 개태,1783,3538,3534,NNP,*,F,개태,Compound,*,*,*)
            morph_inf['POS_type'] = POS.Type.MORPHEME # Compound인데 토큰이 1개니까 그냥 MORPHEME으로 처리
            morph_inf['morphemes'] = None
        else: # 2개 이상: 정상적인 COMPOUND
            morphemes_list = []
            for substr in splits[11].split('+'):
                # substr = 목/NNG/*+매기/NNG/*+송아지/NNG/*
                subword = substr.split('/')[0]
                subpos = substr.split('/')[1]
                #morphemes_list.append(Dictionary.Morpheme(posTag=subpos, surfaceForm=subword))
                morphemes_list.append((subpos, subword))
            morph_inf['morphemes'] = morphemes_list

    #morph_inf['analysis'] = splits[11]
    # 짐수레꾼,1781,3535,2835,NNG,*,T,짐수레꾼,Compound,*,*,짐/NNG/*+수레/NNG/*+꾼/NNG/*
    #sysTokenInfo.insert(token, morph_inf)
    refined_data.append([token, morph_inf])    

# save and compress.
#with gzip.open('mecab_csv.pkl', 'wb') as wf:
#    pickle.dump(sysTokenInfo, wf)

output_f_nm = 'mecab_csv.pkl'
with gzip.open(back_1_path + '/pkl_mecab_csv/' + output_f_nm, 'wb') as wf:
    pickle.dump(refined_data, wf)

#with gzip.open('mecab_csv_trie.pkl', 'rb') as rf:
#    entries = pickle.load(rf) # csv 데이터를 포함한 Trie 자료구조.
#print(entries)

end_main = datetime.now()
print('> {} is successfully generated! - {}'.format(output_f_nm, end_main - start_main))