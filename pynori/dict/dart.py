import sys
import pickle
sys.path.append('/workspaces/python-nori')

import numpy as np
from tqdm import tqdm

from dataclasses import dataclass
from pynori.dict.token_info_ds import TokenInfoDSBase
from typing import List, Tuple

ARRAY_DTYPE = np.dtype([('base', np.int), ('check', np.uintc)])

@dataclass
class Node:
    """
    Node contain trie's left, right node index and it's node depth in trie.
    code means character code (ord(Character))
    ex) A -> 65
    """

    code: int
    depth: int
    left: int
    right: int



class DoubleArrayTrieSystem(TokenInfoDSBase):
    def __init__(self):
        self.keys: List[List[int]] = []
        self.sizes: List[int] = []
        self.key_token_sizes: List[int] = []
        self.error: int = 0
        self.next_check_pos: int = 0
        self.progress: int = 0
        self.size_ = 0
        self.array = np.zeros([], dtype=ARRAY_DTYPE)
        self.used = np.zeros([], dtype=np.bool)
        self.tokens: List[str] = []
        self.dict_pair = []

    def resize(self, size: int):
        self.array = np.resize(self.array, size)
        self.used = np.resize(self.used, size)
    
    def getsizeof(self):
        return sys.getsizeof(self.array) + sys.getsizeof(self.used)
    
    def save(self, filepath):
        with open(filepath, 'wb') as f:
            dump_data = {
                'array': self.array,
                'tokens': self.tokens
            }
            pickle.dump(dump_data, f)
    
    def load(self, filepath):
        with open(filepath, 'rb') as f:
            dump_data = pickle.load(f)
        
        self.array = dump_data['array']
        self.tokens = dump_data['tokens']
    
    def _resize(self, size, target, default_value):
        if len(target) <= size:
            if default_value == 'array':
                target.extend([[0, 0] for _ in range(0, (size - len(target)))])
            else:
                target.extend([False for _ in range(0, (size - len(target)))])
        else:
            del target[size:]

    def decompose_string_to_utf8(self, string):
        """Decompose String to hex values
        Examples:
            Input: 'a한국어'
            Output: [99, 237, 149, 156, 234, 181, 173, 236, 150, 180]
        Args:
            string: string to decompose
        Returns:
            string's integer codes
        """
        return [ord(char) for char in string]
        # return [char for char in string.encode('utf-8')]

    def build(self):
        dict_pair = sorted(self.dict_pair, key=lambda x: x[0])
        bsize = 0
        idx = 0

        prev = None
        str_list = []
        len_list = []
        val_list = []
        self.tokens = [pair[1] for pair in dict_pair]

        for i in range(0, len(dict_pair)):
            if i != 0 and prev != dict_pair[i][0]:
                str_list.append(dict_pair[idx][0])
                len_list.append(len(dict_pair[idx][0]))
                val_list.append(bsize + (idx << 16))
                bsize = 1
                idx = i
            else:
                bsize += 1
            prev = dict_pair[i][0]

        str_list.append(dict_pair[idx][0])
        len_list.append(len(dict_pair[idx][0]))
        val_list.append(bsize + (idx << 16))

        self._build(str_list, len_list, val_list)
        print(len(self.array))
    
    def insert(self, string, result):
        self.dict_pair.append((string, result))

    def _build(self, keys: List[str], sizes: List[int],
              key_token_sizes: List[int]):
        """ Build trie system.
        Args:
            keys: Strings to register in trie
            sizes: An array that collects the lengths of the elements in the key array
            key_token_sizes: An array that collects the token counts of the elements in the key array
        Returns:
            error: Indicate build successfully finished. If this value is non-zero, build is failed.
        """
        print(len(keys), len(sizes), len(key_token_sizes))
        self.keys = [self.decompose_string_to_utf8(key) for key in keys]
        self.sizes = [len(k) for k in self.keys]
        self.key_token_sizes = key_token_sizes
        self.progress = 0
        self.resize(131072)

        self.array[0][0] = 1
        self.next_check_pos = 0
        root_node = Node(code=0, left=0, right=len(keys), depth=0)
        siblings = []
        self.fetch(root_node, siblings)
        print('fetch done', self.getsizeof() / 1024 / 1024)

        self._insert(siblings)
        print('insert done', self.getsizeof() / 1024 / 1024)

        self.size_ += (1 << 17) + 1

        if self.size_ >= len(self.array):
            self.resize(self.size_)

        del self.used
        self.used = None

        return self.error

    def fetch(self, parent: Node, siblings: List[Node]) -> int:
        """ Extract sibling list in parent's left - right range and convert Character to code
        Args:
            parent: trie's parent node
            siblings: List to store sibling Nodes.
        Returns:
            Number of node in siblings
        """
        if self.error < 0:
            return 0

        prev_character_code = 0

        for i in range(parent.left, parent.right):
            if (self.sizes[i]
                    if self.sizes else len(self.keys[i])) < parent.depth:
                continue

            cur_key = self.keys[i]
            cur_character_code = 0

            if (
                self.sizes[i]
                if self.sizes else len(self.keys[i])
            ) != parent.depth:
                cur_character_code = cur_key[parent.depth] + 1

            if prev_character_code > cur_character_code:
                self.error = -3
                return 0

            if prev_character_code != cur_character_code or len(siblings) == 0:
                sibling = Node(code=cur_character_code,
                               depth=parent.depth + 1,
                               left=i,
                               right=-1)
                if len(siblings) != 0:
                    siblings[len(siblings) - 1].right = i
                siblings.append(sibling)

            prev_character_code = cur_character_code

        if len(siblings) != 0:
            siblings[len(siblings) - 1].right = parent.right

        return len(siblings)

    
    def _insert(self, siblings: List[Node]) -> int:
        """ Insert prefetch siblings into parent node.
        Assign base and check values.
        Args:
            siblings: Node list to add into trie.
        Returns:
            node's begin index of double array (self.array)
        """
        if self.error < 0:
            return 0

        begin: int = 0
        pos: int = max(siblings[0].code + 1, self.next_check_pos) - 1
        nonzero_num: int = 0
        first: bool = True

        if len(self.array) <= pos:
            print('resize', len(self.array), pos, siblings[0].code, self.getsizeof() / 1024 / 1024)
            self.resize(pos + 1)
        
        iter_count = 0
        while True:
            iter_count += 1
            is_pass = True
            pos += 1

            if len(self.array) <= pos:
                print('resize', len(self.array), pos, siblings[0].code, self.getsizeof() / 1024 / 1024)
                self.resize(pos + 1)

            if self.array[pos][1]:
                nonzero_num += 1
                continue
            elif first:
                self.next_check_pos = pos
                first = False

            begin = pos - siblings[0].code

            if len(self.array) <= (begin + siblings[-1].code):
                print('before resize', len(self.array), pos, siblings[0].code, self.getsizeof() / 1024 / 1024)
                self.resize(
                    len(self.array) *
                    int(max(1.05, 1.0 * len(self.keys) / (self.progress + 1))))
                print('after resize', len(self.array), pos, siblings[0].code, self.getsizeof() / 1024 / 1024)

            if self.used[begin]:
                continue

            for i in range(1, len(siblings)):
                # print(len(self.array), begin + siblings[i].code)
                if self.array[begin + siblings[i].code][1] != 0:
                    is_pass = False
                    break

            if is_pass:
                break

        # -- Simple heuristics --
        # if the percentage of non-empty contents in check between the index
        # 'next_check_pos' and 'check' is greater than some constant
        # value(e.g. 0.9),
        # new 'next_check_pos' index is written by 'check'.

        if 1.0 * nonzero_num / (pos - self.next_check_pos + 1) >= 0.95:
            self.next_check_pos = pos

        self.used[begin] = True
        self.size_ = max(self.size_, begin + siblings[-1].code + 1)

        for i in range(0, len(siblings)):
            self.array[begin + siblings[i].code][1] = begin


        iters = range(0, len(siblings))
        if begin == 1:
            iters = tqdm(iters, total=len(siblings))

        for i in iters:
            new_siblings: List[Node] = []

            if self.fetch(siblings[i], new_siblings):
                h: int = self._insert(new_siblings)
                self.array[begin + siblings[i].code][0] = h
            else:
                self.array[begin + siblings[i].code][0] = (
                    -self.key_token_sizes[siblings[i].left] -
                    1 if self.key_token_sizes else -siblings[i].left - 1)

                if self.key_token_sizes and -self.key_token_sizes[
                        siblings[i].left] - 1 >= 0:
                    self.error = -2
                    return 0

                self.progress += 1

        return begin

    def search(self, key: str):
        """ Find exact match string in trie.
        Args:
            key: search key for exact match
            size: key length.
            node_pos: root index.
        Returns:
            dict of str: int
            {
                'value': int. input key's number of token
                'len': int. input key's length
            }
        """
        size: int = 0
        node_pos: int = 0
        key = self.decompose_string_to_utf8(key)
        if not size:
            size = len(key)

        results = []

        base: int = self.array[node_pos][0]
        pointer: int

        for i in range(0, size):
            pointer = base + key[i] + 1
            if base == self.array[pointer][1]:
                base = self.array[pointer][0]
            else:
                if len(results) != 0:
                    return (True, results)
                else:
                    return (False, None)
        pointer = base
        value = self.array[pointer][0]

        if base == self.array[pointer][1] and value < 0:
            results.extend(self.get_tokens(-value - 1))

        if len(results) != 0:
            return (True, results)
        else:
            return (False, None)

    def common_prefix_search(self,
                             key: str,
                             size: int = 0,
                             node_pos: int = 0):
        """ Find prefix match string in trie.
        Args:
            key: search key for exact match
            result_len: max number of result prefixes
            size: key length.
            node_pos: root index.
        Returns:
            list of dict of str: int
            [{
                'value': int. input key's number of token
                'len': int. input key's length
            }]
        """
        key = self.decompose_string_to_utf8(key)
        if not size:
            size = len(key)

        results = []
        base: int = self.array[node_pos][0]
        pointer: int

        for i in range(0, size):
            pointer = base
            value = self.array[pointer][0]

            if base == self.array[pointer][1] and value < 0:
                results.extend(self.get_tokens(-value - 1))

            pointer = base + key[i] + 1
            if base == self.array[pointer][1]:
                base = self.array[pointer][0]
            else:
                return results

        pointer = base
        value = self.array[pointer][0]

        if base == self.array[pointer][1] and value < 0:
            results.extend(self.get_tokens(-value - 1))

        return results
    
    def get_tokens(self, value):
        """ Convert trie node info to tokens
        Args:
            value: trie node info
        Returns:
            list of str
                ['TOKEN1', 'TOKEN2' ...]
        """
        if(value < 0):
            return []

        token_start = value >> 16
        token_len = value & 0xffff
        return self.tokens[token_start:token_start + token_len]


if __name__ == "__main__":
    da = DoubleArrayTrieSystem()

    token_list = ['자연어처리', '자연', '인공지능', '자', '자연어처리하자']

    token_info = dict()
    token_info['자연어처리'] = ['<자연어처리 - 토큰 정보>', '<자연어처리 - 토큰 정보2>', '<자연어처리 - 토큰 정보3>']
    token_info['자연'] = ['<자연 - 토큰 정보>', '<자연 - 토큰 정보2>']
    token_info['인공지능'] = ['<인공지능 - 토큰 정보>']
    token_info['자'] = ['<자 - 토큰 정보>']
    token_info['자연어처리하자'] = ['<자연어처리하자 - 토큰 정보>']
    

    for parent in token_list:
        for token in token_info[parent]:
            da.insert(parent, token)
    
    da.build()
    token_list.append("헬로우")
    for token in token_list:
        print(token)
        print(da.search(token))
        print('\n')