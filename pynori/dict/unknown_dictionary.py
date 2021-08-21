import os
from pathlib import Path
from configparser import ConfigParser

from pynori.dict.dictionary import Dictionary
from pynori.dict.character_definition import CharacterDefinition
from pynori.dict.token_info_ds import DSManager
from pynori.pos import POS

cfg = ConfigParser()
dir_path = Path(os.path.dirname(os.path.abspath(__file__)))
PATH_CUR = str(dir_path.parent)
cfg.read(PATH_CUR+'/config.ini')
TOKEN_INFO_DS = cfg['OPTION']['TOKEN_INFO_DS']


class UnknownDictionary(Dictionary):
	"""Build Unknown Dictionary

	Loaded words will be used as unknown tokens.
	"""

	@staticmethod
	def open(UNK_PATH):
		entries = []
		with open(UNK_PATH, 'r', encoding='UTF8') as rf:
			for line in rf:
				line = line.strip()
				if len(line) == 0:
					continue
				entries.append(line)
		if len(entries) == 0:
			return None
		else:
			return UnknownDictionary(entries)

	def __init__(self, entries):
		charDef = CharacterDefinition()
		entries = sorted(entries)
		self.unkTokenInfo = DSManager.get_ds(TOKEN_INFO_DS)

		for entry in entries:
			splits = entry.split(',')
			morph_inf = dict()
			morph_inf['surface'] = splits[0]
			morph_inf['left_id'] = splits[1]
			morph_inf['right_id'] = splits[2]
			morph_inf['word_cost'] = int(splits[3])
			morph_inf['POS'] = splits[4]
			morph_inf['POS_type'] = POS.Type.MORPHEME # 임시방편
			morph_inf['morphemes'] = None
			# splits[0] : DEFAULT
			# ','.join(splits[1:]) : 1801,3566,3640,SY,*,*,*,*,*,*,*
			self.unkTokenInfo.insert(splits[0], morph_inf)

"""
	#@override
	def getLeftId(self, wordId):
		return None
	
	#@override
	def getRighId(self, wordId):
		return None
		
	#@override
	def getWordCost(self, wordId):
		return None
		
	#@override
	def getPOSType(self, wordId):
		return None
	
	#@override
	def getLeftPOS(self, wordId):
		return None
		
	#@override
	def getRightPOS(self, wordId):
		return None
"""