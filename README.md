# pynori

Python package for [nori](https://github.com/apache/lucene-solr/tree/master/lucene/analysis/nori), which is the korean morpological analyzer in the [Apache Lucene](https://github.com/apache/lucene-solr).

자바로 작성되어 있는 아파치 루씬의 노리 형태소 분석기를 파이썬으로 변환한 프로젝트입니다. 원본과 같은 테스트를 실시하여 동일한 결과를 얻었습니다(ref.Test). 동의어 확장 필터는 제외하고 다른 기능은 모두 정상적으로 동작합니다. 정확도는 동일하지만 파이썬 언어인 점과 더불어 Trie 자료구조의 사용 등으로 속도는 조금 느립니다(ref.Property). 진행하지 못한 일들은 앞으로 보완할 계획입니다(ref.TODO).

노리 형태소 분석기에 대한 내용은 저의 [노리 Deep Dive 블로그](https://gritmind.github.io/2019/05/nori-deep-dive.html)를 참고해주세요.


## Usage

```python
# Usage-1. 'config' file
>>> from pynori.korean_analyzer import KoreanAnalyzer
>>> nori = KoreanAnalyzer()
>>> nori.do_analysis("아빠가 방에 들어가신다.")
{'termAtt': ['아빠', '가', '방', '에', '들어가', '시', 'ᆫ다'],
 'offsetAtt': [(0, 2), (2, 3), (4, 5), (5, 6), (7, 10), (10, 12), (10, 12)],
 'posLengthAtt': [1, 1, 1, 1, 1, 1, 1],
 'posTypeAtt': ['MORP', 'MORP', 'MORP', 'MORP', 'MORP', 'MORP', 'MORP'],
 'posTagAtt': ['NNG', 'JKS', 'NNG', 'JKB', 'VV', 'EP', 'EF'],
 'dictTypeAtt': ['KN', 'KN', 'KN', 'KN', 'KN', 'KN', 'KN']}
 
# Usage-2. argument
>>> from pynori.korean_analyzer import KoreanAnalyzer
>>> nori = KoreanAnalyzer(decompound_mode='MIXED',
                          discard_punctuation=False,
			  			  output_unknown_unigrams=True,
                          pos_filter=True,
                          stop_tags=['JKS', 'JKB', 'VV', 'EF'])
>>> nori.do_analysis("아빠가 방에 들어가신다.")
{'termAtt': ['아빠', ' ', '방', ' ', '신다', '시', '.'],
 'offsetAtt': [(0, 2), (3, 4), (4, 5), (6, 7), (10, 12), (10, 12), (12, 13)],
 'posLengthAtt': [1, 1, 1, 1, 2, 1, 1],
 'posTypeAtt': ['MORP', 'MORP', 'MORP', 'MORP', 'INFL', 'MORP', 'MORP'],
 'posTagAtt': ['NNG', 'SP', 'NNG', 'SP', 'EP+EF', 'EP', 'SF'],
 'dictTypeAtt': ['KN', 'UKN', 'KN', 'UKN', 'KN', 'KN', 'KN']}
```

## Test

```
$ python -m unittest -v tests.test_korean_analyzer
$ python -m unittest -v tests.test_korean_tokenizer
```

## Property

* Use mecab-ko-dic-2.1.1-20180720
* Based on lucene korean analyzer, nori
* Start with config.ini file and initialize object
* Use Trie data structure, instead of FST
* Modify token & dictionary objects
* Not use circular buffer
* Not use wordID

## TODO

* Synonym Graph Filter
* KoreanTokenizer TODO List (MAX_BACKTRACE_GAP, isLowSurrogate, UnicodeScript ...)

## Reference
* [Lucene-solr Github](https://github.com/apache/lucene-solr/tree/master/lucene/analysis/nori)
* [Mecab-ko-dic](https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/)