"""
bi-gram connection cost data from mecab

Reference: matrix.def
"""

import os


class ConnectionCosts(object):
	"""n-gram connection cost data
	"""

	def open(COST_PATH): # 주의: self 는 여기서 필요없음.

		entries = []
		#with open(COST_PATH, 'r') as rf:
		#	for line in rf:
		#		ine = line.strip()
		#		if len(line) == 0:
		#			continue
		#		entries.append(line)

		for dirName, subdirList, fileList in os.walk(COST_PATH):
			for fname in fileList:
				if fname.split('.')[-1] == 'txt':
					PATH_EACH = dirName + '/' + fname
					
					with open(PATH_EACH, 'r', encoding='UTF8') as rf: 
						for line in rf:
							line = line.strip()
							if len(line) == 0:
								continue
							entries.append(line)


		if len(entries) == 0:
		    return None
		else:
		    return ConnectionCosts(entries)

	def __init__(self, entries):
			
		self.conCosts = dict()

		for entry in entries:
			splits = entry.split()
			if len(splits) != 3:
				continue

			rightId = int(splits[0])
			leftId = int(splits[1])
			cost = int(splits[2])

			self.conCosts[(rightId, leftId)] = cost

		
	def get(self, rightId, leftId):
		return self.conCosts[(int(rightId), int(leftId))]
		