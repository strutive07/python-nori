
import sys
sys.path.append('/workspaces/python-nori')
from abc import abstractmethod


class DSManager:
    """ Data Structure Manager
        selects data structure for saving tokens with morphologinal analysis results by Mecab-ko-dic
    """
    @staticmethod 
    def get_ds(name): # get a specific data structure
        if name == "trie":
            return Trie()
        elif name == "py-dict":
            return Dict()
        elif name == 'dart':
            from pynori.dict.dart import DoubleArrayTrieSystem
            return DoubleArrayTrieSystem()
        elif name == "fst":
            print("fst is not implemented yet")
            exit()
 
class TokenInfoDSBase:
	@abstractmethod
	def insert(self):
		pass
	@abstractmethod
	def search(self):
		pass
	@abstractmethod
	def build(self):
		pass


class Dict(TokenInfoDSBase):
    def __init__(self):
        self.mydict = {}
    def insert(self, string, result):
        if self.mydict.get(string) is None:
            self.mydict[string] = [result]
        else:
            if result not in self.mydict[string]:
                self.mydict[string].append(result)
    def search(self, string):
        if self.mydict.get(string) is not None:
            if self.mydict[string] == -1:
                return (True, None)
            else:
                return (True, self.mydict[string])
        else:
            return (False, None)
    def build(self):
        pass


class Trie(TokenInfoDSBase):
    def __init__(self):
        self.head = Node(key=None)
    def insert(self, string, result):
        cur_node = self.head # pivot
        for char_key in string:
            if char_key not in cur_node.children:
                cur_node.children[char_key] = Node(char_key) # make node
            cur_node = cur_node.children[char_key] # update pivot
            #cur_node.flag_end = False # re-init for new overlapping string, while iterating.
            #cur_node.flag_ing = True
        # now cur_node is leaf node
        #if len(cur_node.children) == 0: # leaf-node: not have child node
        #    cur_node.flag_end = True
        cur_node.data = string
        if result not in cur_node.result:
            cur_node.result.append(result)
    def search(self, string):
        cur_node = self.head
        for char_key in string:
            if char_key in cur_node.children:
                cur_node = cur_node.children[char_key]
            else:
                return (False, None)
                #return cur_node
        if cur_node.data is not None:
            return (True, cur_node.result) # cur_node.result or cur_node.flag
        return (True, None)
    def build(self):
        pass

class Node:
    def __init__(self, key, data=None, result=None):
        self.key = key
        self.data = data
        #self.flag_ing = False
        #self.flag_end = False # whether or not leaf node 
        self.result = []
        if result is not None:
            self.result.append(result)
        self.children = dict()


if __name__ == "__main__":

    test_trie = DSManager.get_ds("dart")

    token_list = ['자연어처리', '자연', '인공지능', '자', '자연어처리하자']

    token_info = dict()
    token_info['자연어처리'] = '<자연어처리 - 토큰 정보>'
    token_info['자연'] = '<자연 - 토큰 정보>'
    token_info['인공지능'] = '<인공지능 - 토큰 정보>'
    token_info['자'] = '<자 - 토큰 정보>'
    token_info['자연어처리하자'] = '<자연어처리하자 - 토큰 정보>'

    for token in token_list:
        test_trie.insert(token, token_info[token])
    test_trie.build()

    ##
    token_list.append("헬로우")
    for token in token_list:
        print(test_trie.search(token))
        print(test_trie.search(token)[-1])
        #print(test_trie.search(token)[-1].flag)
        print('\n')