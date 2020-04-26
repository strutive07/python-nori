# Pynori

Pynori is python version of Nori, Korean Analyzer in Apache Lucene and Elasticsearch.

* Nori
   * 아파치 루씬 및 엘라스틱서치에 포함된 한국어 형태소 분석기 플러그인 (자바로 작성)
   * mecab / kuromoji 기반의 한국어 형태소 분석기 (mecab-ko-dic-2.1.1-20180720 사용)
   * 루씬 또는 엘라스틱서치 엔진에 종속된 한국어 형태소 분석기
* Pynori
   * Nori의 파이썬 버전 & 순수 파이썬 스크립트로 작성 (ref.Property & Comparision Study)
   * 원본과 같은 유닛테스트를 실시하여 동일한 결과를 얻음. (ref.Test)
   * 독립된 모듈로 파이썬 프로젝트 활용 가능
   * 원본 Nori 대비 개선 기능 (ref.Property)

노리 형태소 분석기에 대한 내용은 [노리 Deep Dive 블로그](https://gritmind.github.io/2019/05/nori-deep-dive.html)를 참고해주세요.

pynori에 대한 이슈 사항은 [issue](https://github.com/gritmind/python-nori/issues)에 등록해주세요. 


## Install

```
pip install pynori
```

## Usage

```python
from pynori.korean_analyzer import KoreanAnalyzer
nori = KoreanAnalyzer(decompound_mode='MIXED',
                      infl_decompound_mode='DISCARD',
                      discard_punctuation=True,
                      output_unknown_unigrams=False,
                      pos_filter=False, stop_tags=['JKS', 'JKB', 'VV', 'EF'])

print(nori.do_analysis("아빠가 방에 들어가신다."))
```
```
{'termAtt': ['아빠', '가', '방', '에', '들어가', '시', 'ᆫ다'],
 'offsetAtt': [(0, 2), (2, 3), (4, 5), (5, 6), (7, 10), (10, 12), (10, 12)],
 'posLengthAtt': [1, 1, 1, 1, 1, 1, 1],
 'posTypeAtt': ['MORP', 'MORP', 'MORP', 'MORP', 'MORP', 'MORP', 'MORP'],
 'posTagAtt': ['NNG', 'JKS', 'NNG', 'JKB', 'VV', 'EP', 'EF'],
 'dictTypeAtt': ['KN', 'KN', 'KN', 'KN', 'KN', 'KN', 'KN']}
```

* `KoreanAnalyzer` arg.
   * `decompound_mode` / `infl_decompound_mode` - 복합명사 / 굴절어 처리 방식 결정
      * 'MIXED': 원형과 서브단어 모두 출력
      * 'DISCARD': 서브단어만 출력
      * 'NONE': 원형만 출력
   * `discard_punctuation` - 구두점 제거 여부
   * `output_unknown_unigrams` - 언논 단어를 음절 단위로 쪼갬 여부
   * `pos_filter` - POS 필터 실행 여부
   * `stop_tags` - 필터링되는 POS 태그 리스트 (pos_filter=True일 때만 활성)

다음과 같이 KoreanAnalyzer의 옵션을 동적으로 제어할 수 있습니다.

```python
print(nori.do_analysis("가벼운 냉장고")['termAtt'])

nori.set_option_tokenizer(decompound_mode='DISCARD', infl_decompound_mode='MIXED')
print(nori.do_analysis("가벼운 냉장고")['termAtt'])

nori.set_option_filter(pos_filter=True, stop_tags=['ETM', 'VA'])
print(nori.do_analysis("가벼운 냉장고")['termAtt'])
```
```
['가볍', 'ᆫ', '냉장고', '냉장', '고']
['가벼운', '가볍', 'ᆫ', '냉장', '고']
['냉장', '고']
```


## Resources

* 시스템 사전은 `~/pynori/resources/mecab-ko-dic-2.1.1-20180720` 에서 수정
   * (mecab 규칙 준수 필요) 기존 csv 파일 수정/삭제 or 새로운 csv 파일 추가
   * 사전 변경사항은 `~/pynori/resources/pkl_mecab_csv/mecab_csv.pkl` 를 삭제하면 적용 o
   * (`mecab_csv.pkl` 파일이 없으면 KoreanAnalyzer 초기화 시에 최신 csv 파일을 기반으로 재생성됨)
* 사용자 사전은 `~/pynori/resources/userdict_ko.txt` 에서 수정만 하면 자동 적용 o
* 동의어 사전은 `~/pynori/resources/synonyms.txt.txt` 에서 수정만 하면 자동 적용 o

## Test

```
git clone https://github.com/gritmind/python-nori.git
cd python-nori
python -m unittest -v tests.test_korean_analyzer
python -m unittest -v tests.test_korean_tokenizer
```


## Property

* [원본] 루씬(lucene), 노리(nori) 형태소 분석기 (ref.1)
* 원본 코드와 최대한 비슷하게 구현 (변수/파일명, 코드 패턴 등)
* 언어 리소스로 `mecab-ko-dic-2.1.1-20180720` 사용
* 사전 룩업을 위해 Trie 자료구조 사용 (instead of FST)
* token & dictionary objects 수정
* circular buffer & wordID 삭제

_원본 Nori 대비 개선 기능_

* 토큰 정보 (Unknown/Known/User, POS type) 출력
* 특수문자로 시작/포함하는 사용자 단어가 있을 시 동의어 파싱 오류 해결
* infl_decompound_mode 모드 추가
* KoreanAnalyzer 옵션을 동적으로 제어하는 기능 추가


## TODO

* 동의어 확장 필터
* 필터 후 토큰 인덱스/포지션 재배열
* KoreanTokenizer TODO List (MAX_BACKTRACE_GAP, isLowSurrogate, UnicodeScript ...)
* 속도 향상을 위한 알고리즘 및 자료구조 최적화
* Unknown 길이가 무분별하게 길어지는 현상 해결


## Comparision Study

|                 | 한나눔 0.8.4      | 꼬꼬마 2.0     | 트위터 1.14.7   | Pynori 0.1.0    |
| :-------------: | :-------------: |:-------------:|:-------------:|:-------------:|
| 1 개             | 0.00138 sec     | 0.00244 sec   | 0.00051 sec    | 0.00279 sec   |
| 10 개            | 0.03467 sec     | 0.07546 sec   | 0.01188 sec    | 0.09655 sec   |
| 100 개           | 0.28960 sec     | 0.70480 sec   | 0.09319 sec    | 0.72207 sec   |
| 1000 개          | 2.59061 sec     | 6.38031 sec   | 0.94029 sec    | 6.46660 sec   |
| 10000 개         | 27.61180 sec     | 77.73616 sec   | 11.43677 sec    | 68.20249 sec   |
| 100000 개        | 262.72305 sec     | 699.70416 sec   | 95.79926 sec    | 672.83272 sec   |

* 데이터를 증가시키면서 다양한 종류의 한국어 형태소 분석기와 처리 속도를 비교. (참고 `./tests/test_compare_morphs.py`). 
* 비교 대상은 모두 파이썬 라이브러리(konlpy)에 모두 속해 있지만 내부적으로 JVM 기반으로 동작함. 
* pynori는 순수 파이썬 스크립트로 실행되지만, 트위터를 제외하고는 큰 차이가 발생하지 않고, 꼬꼬마 2.0보다는 빠름.

## Release History

| 버전             | 주요 내용             | 날짜     |
| :-------------: | :-------------: | :-----: |
| pynori 0.1.0    | 기본적인 노리 파이썬 패키지 포팅 & & 유닛테스트 구현 완료 | Nov 17, 2019 |
| pynori 0.1.1    | KoreanAnalyzer 초기화 속도 향상 (1min 15s -> 12.9s)     | Apr 16, 2020 |
| pynori 0.1.2    | infl_decompound_mode 모드 추가                        | Apr 23, 2020 |
| pynori 0.1.3    | KoreanAnalyzer 옵션을 동적으로 제어하는 기능 추가           | Apr 25, 2020 |


## License

* Apache License 2.0

## Reference
1. (Github) [Lucene-solr - Nori](https://github.com/apache/lucene-solr/tree/master/lucene/analysis/nori)
2. (Github) [Mecab-ko-dic](https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/)
3. (Blog) [엘라스틱서치 공식 한국어 분석 플러그인 '노리'](https://www.elastic.co/kr/blog/nori-the-official-elasticsearch-plugin-for-korean-language-analysis)
4. (Blog) [노리(Nori) 형태소 분석기 Deep Dive](https://gritmind.github.io/2019/05/nori-deep-dive.html)
