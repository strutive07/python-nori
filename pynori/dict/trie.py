
class Node(object):
    def __init__(self, key, data=None, result=None):
        self.key =  key
        self.data = data
        self.result = []
        if result is not None:
            self.result.append(result)
        self.children = dict()

		
class Trie(object):
    """Trie Data Structure

    Data Structure for saving tokens with 
    morphologinal analysis results by Mecab-ko-dic
    """

    def __init__(self):
        self.head = Node(key=None)
        
    def insert(self, string, result):
        cur_node = self.head # pivot
        
        for char_key in string:
            if char_key not in cur_node.children:
                cur_node.children[char_key] = Node(char_key) # make node
            cur_node = cur_node.children[char_key] # update pivot
            
        # now cur_node is leaf node
        cur_node.data = string
        if result not in cur_node.result:
            cur_node.result.append(result)
        
    def search(self, string):
        cur_node = self.head
        
        for char_key in string:
            if char_key in cur_node.children:
                cur_node = cur_node.children[char_key]
            else:
                return None # False
            
        if cur_node.data != None:
            return cur_node.result # True