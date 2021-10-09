
"""
    Usage:
        python -m pynori.tests.test_execute_time
"""

import os
import sys
import random
from pathlib import Path
sys.path.append('/workspaces/python-nori')

from konlpy.tag import Hannanum
from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Okt

from pynori.korean_analyzer import KoreanAnalyzer
from pynori.utils import *
from tqdm import tqdm


file_path = Path(os.path.dirname(os.path.abspath(__file__)))
workspace_path = file_path

news_path = str(workspace_path) + '/news_body_1m.csv'
shopping_path = str(workspace_path) + '/shopping_title_1m.csv'

print(workspace_path)
print(shopping_path)

@calc_execution_time
def run_analyzer_with_data(analyzer_obj, data):
    cname = analyzer_obj.__class__.__name__
    print(cname)
    err_cnt = 0 
    for x in tqdm(data):
        try:
            if cname == 'KoreanAnalyzer':
                analyzer_obj.do_analysis(x)
            else:
                analyzer_obj.pos(x)
        except:
            raise
            err_cnt += 1
            pass
    print('err_cnt: ', err_cnt)
    return


if __name__ == '__main__':

    news_data = load_lines(news_path)
    shop_data = load_lines(shopping_path)

    # hannanum = Hannanum()
    # kkma = Kkma()
    # komoran = Komoran()
    # okt = Okt()
    nori = KoreanAnalyzer(decompound_mode='MIXED',
                          discard_punctuation=True,
                          output_unknown_unigrams=True,
                          pos_filter=False,
                          stop_tags=['JKS', 'JKB', 'VV', 'EF'])

    data = news_data + shop_data
    random.seed(7)
    data = random.sample(data, 1000000)
    print('number of total data: ', len(data))
    print()

    for idx in [
        # 100, 
        # 1000, 
        # 10000, 
        100000, 
        # 1000000
    ]:
        sample_data = data[:idx]
        print('\n number of sample data: ', len(sample_data))

        for analyzer in [nori]:
            run_analyzer_with_data(analyzer, sample_data)
            print()