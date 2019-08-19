import os
from configparser import ConfigParser

from pynori.src.korean_tokenizer import KoreanTokenizer
from pynori.src.korean_posstop_filter import KoreanPOSStopFilter
from pynori.src.synonym_graph_filter import SynonymGraphFilter
from pynori.src.preprocessing import Preprocessing


cfg = ConfigParser()
PATH_CUR = os.getcwd()+'/pynori'
cfg.read(PATH_CUR+'/config.ini')

# PREPROCESSING
ENG_LOWER = cfg.getboolean('PREPROCESSING', 'ENG_LOWER')
# OPTION
DECOMPOUND_MODE = cfg['OPTION']['DECOMPOUND_MODE']
VERBOSE = cfg.getboolean('OPTION', 'VERBOSE')
OUTPUT_UNKNOWN_UNIGRAMS = cfg.getboolean('OPTION', 'OUTPUT_UNKNOWN_UNIGRAMS')
DISCARD_PUNCTUATION = cfg.getboolean('OPTION', 'DISCARD_PUNCTUATION')
# FILTER
USE_SYNONYM_FILTER = cfg.getboolean('FILTER', 'USE_SYNONYM_FILTER')
USE_POS_FILTER = cfg.getboolean('FILTER', 'USE_POS_FILTER')
# PATH
PATH_USER_DICT = cfg['PATH']['USER_DICT']


class KoreanAnalyzer(object):
	"""Analyzer for Korean that uses morphological analysis.
	"""

	def __init__(self, 
				 verbose=VERBOSE,
				 path_userdict=PATH_USER_DICT,
				 decompound_mode=DECOMPOUND_MODE,
				 output_unknown_unigrams=OUTPUT_UNKNOWN_UNIGRAMS,
				 discard_punctuation=DISCARD_PUNCTUATION,
				 pos_filter=USE_POS_FILTER,
				 stop_tags=KoreanPOSStopFilter.DEFAULT_STOP_TAGS,
				 synonym_filter=USE_SYNONYM_FILTER):
		self.kor_tokenizer = KoreanTokenizer(verbose, path_userdict, decompound_mode, output_unknown_unigrams, discard_punctuation)
		self.kor_pos_filter = KoreanPOSStopFilter(stop_tags=stop_tags)
		self.syn_graph_filter = SynonymGraphFilter()
		self.pos_filter = pos_filter
		self.synonym_filter = synonym_filter

	def do_analysis(self, in_string):
		"""Analyze text data
		   (1) Preprocessing
		   (2) Tokenizing
		   (3) Filtering
		"""

		# Preprocessing
		if ENG_LOWER:
			in_string = Preprocessing.lower(in_string)
		#in_string = Preprocessing.typo(in_string)
		#in_string = Preprocessing.spacing(in_string)

		# Tokenizing
		self.kor_tokenizer.set_input(in_string)
		while self.kor_tokenizer.increment_token():
			pass
		tkn_attr_obj = self.kor_tokenizer.tkn_attr_obj

		# POS Filtering
		if self.pos_filter:
			tkn_attr_obj = self.kor_pos_filter.do_filter(tkn_attr_obj)

		# Synonym Filtering
		if self.synonym_filter:
			tkn_attr_obj = self.syn_graph_filter.do_filter(tkn_attr_obj)

		return tkn_attr_obj.__dict__
