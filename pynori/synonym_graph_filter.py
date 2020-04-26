import os
from configparser import ConfigParser
from pynori.dict.trie import Trie


cfg = ConfigParser()
#PATH_CUR = os.getcwd() + '/pynori'
PATH_CUR = os.path.dirname(__file__)
cfg.read(PATH_CUR+'/config.ini')

# PATH
PATH_SYN_DICT = cfg['PATH']['SYN_DICT']



class SynonymGraphFilter(object):
	"""Synonym Text Processing

	Add synonym words to token stream / or Norm synonmy words
	keeping token offsets.

	Parameters
	----------
	kor_tokenizer

	synonym_mode : {'EXTENSION', 'NORM'}
	
	"""

	def __init__(self, kor_tokenizer, synonym_mode):
		self.tokenizer = kor_tokenizer
		self.synonym_mode = synonym_mode
		#self.entries = self.open(PATH_CUR+PATH_SYN_DICT)
		pass

	def open(self, path_syn_file):
		entries = []
		with open(path_syn_file, 'r', encoding='utf-8') as rf:
			for line in rf:
				line = line.strip()
				entries.append(line)
		return entries

	# [ TODO ] - 동의어 관련 데이터 저장
	# Trie 를 활용하여 동의어 단어 룩업 구조 구현
	# Trie 에는 key는 토큰을, value는 동의어 리스트 또는 동의어 대표어를 할당 (저장 시 토크나이징 결과 반영)
	# 토크나이징 결과를 (id, 결과) 형태로 dict 에 저장 -> Trie 에 id만 저장


	def do_filter(self, tkn_attrs):

		# [ TODO ] - 동의어 필터링 방식
		# 토크나이징 모드(MIXED, DISCARD, NONE)에 상관없이 동작해야 함
		# ['lg', 'tv', '냉장', '고']
		# 왼쪽에서 오른쪽으로 늘리면서 Trie 룩업 체크.
		# 'lg' 룩업 -> (O) -> [X]
		# 'lg_tv' 룩업 -> (O) -> [O]
		## 'lg_tv'에서 Trie를 더이상 내려가지 않아도 된다는 흔적이 있으면? 굳이 'lg_tv_냉장'을 룩업할 필요 x.
		## Trie에 데이터를 넣을 때, 정렬 후 가장 긴 길이부터 항상 넣고, 넣을 때, 이게 마지막이라는 flag 정보도 함께 넣는다면.?
		# 'lg_tv_냉장' 룩업 -> [X]
		# '냉장' 룩업 -> (O) -> [X]
		# '냉장_고' 룩업 -> (O) -> [O]
		# 다음 토큰 없음.
		# Trie 룩업 횟수를 최소화할 수 있는 방안 필요
		# Trie 룩업의 마지막 위치를 기억할 수 있는 기능 필요 (토큰이 짧지만, 횟수가 많기 때문에 유의미할 듯)
		# Trie 에서 찾아들어가는 위치를 캐쉬할 수 있나?
		# Trie 룩업은 항상 처음부터 시작해야 하나?

		return tkn_attrs

