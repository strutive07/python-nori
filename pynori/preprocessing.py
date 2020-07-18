import os
from configparser import ConfigParser

cfg = ConfigParser()
#PATH_CUR = os.getcwd() + '/pynori'
PATH_CUR = os.path.dirname(__file__)
cfg.read(PATH_CUR+'/config.ini')

# PREPROCESSING
ENG_LOWER = cfg.getboolean('PREPROCESSING', 'ENG_LOWER')

class Preprocessing(object):
	"""Preprocessing modules before tokenizing
	   
	   It doesn't need to be initialized.
	"""

	def __init__(self):
		pass
	
	def pipeline(self, input_str):
		""" the sequence of preprocessing modules.
		"""

		# Lower
		if ENG_LOWER:
			input_str = self._lower(input_str)
		
		# ...

		return input_str

	def _lower(self, input_str):
		"""To lower input string"""
		return input_str.lower()
		
	def _typo(self, input_str):
		"""To correct typing errors"""
		pass
		
	def _spacing(self, input_str):
		"""To correct spacing errors"""
		pass
	
	