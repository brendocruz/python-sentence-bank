from enum import IntEnum
from typing import cast

type TrieChildren = dict[str, 'TrieNode']
type TrieNode = list[TrieChildren | bool]


class _Attribute(IntEnum):
    TERMINAL = 0
    CHILDREN = 1


class Trie:
    _root: TrieNode

    WILDCARD_SINGLE = '?'
    WILDCARD_MULTI  = '*'

    def __init__(self, root: TrieNode | None = None) -> None:
        self._root = root or self._create_root()

    def _create_root(self) -> TrieNode:
        root = [False, {}]
        return root

    def _create_node(self, parent: TrieNode, key: str, is_terminal: bool) -> None:
        new_node: TrieNode = [is_terminal, {}]
        children = cast(TrieChildren, parent[_Attribute.CHILDREN])
        children[key] = new_node

    def insert(self, term: str) -> bool:
        if term == '':
            return False

        is_new          = False
        current         = self._root
        last_char_index = len(term) - 1
        for index, char in enumerate(term):
            children    = cast(TrieChildren, current[_Attribute.CHILDREN])
            is_terminal = index == last_char_index
            if char not in children:
                is_new = True
                self._create_node(current, char, is_terminal)
            current = children[char]
            if is_terminal:
                is_new = is_new or current[_Attribute.TERMINAL] == False
                current[_Attribute.TERMINAL] = True
        return is_new

    def contains(self, term: str) -> bool:
        if term == '':
            return False

        current         = self._root
        last_char_index = len(term) - 1
        for index, char in enumerate(term):
            children = cast(TrieChildren, current[_Attribute.CHILDREN])
            if char not in children:
                return False
            current  = children[char]
            if index != last_char_index:
                continue
            if current[_Attribute.TERMINAL]:
                return True
            break
        return False

    def remove(self, term: str) -> bool:
        if term == '':
            return False

        current         = self._root
        last_char_index = len(term) - 1
        last_fork       = current
        key_to_prune    = term[0]
        for index, char in enumerate(term):
            children = cast(TrieChildren, current[_Attribute.CHILDREN])
            if char not in children:
                return False

            if current[_Attribute.TERMINAL] or len(children) > 1:
                last_fork    = current
                key_to_prune = char
            current = children[char]

            if index < last_char_index:
                continue
            if not current[_Attribute.TERMINAL]:
                return False
            current[_Attribute.TERMINAL] = False

        children = cast(TrieChildren, current[_Attribute.CHILDREN])
        if len(children) > 0:
            last_fork = None

        if last_fork is None:
            return True

        fork_children = cast(TrieChildren, last_fork[_Attribute.CHILDREN])
        fork_children.pop(key_to_prune)
        return True

    def _search_node(self, node: TrieNode, pattern: str, path: str) -> list[str]:
        terminal = cast(bool, node[_Attribute.TERMINAL])
        if pattern == '':
            if not terminal:
                return []
            return [path]

        children = cast(TrieChildren, node[_Attribute.CHILDREN])
        char     = pattern[0]

        if char == '?':
            matched: list[str] = []
            for child_key, child_node in children.items():
                matches = self._search_node(child_node, pattern[1:], path + child_key)
                matched.extend(matches)
            return matched

        if char == '*':
            matched: list[str] = []

            matches = self._search_node(node, pattern[1:], path)
            matched.extend(matches)

            for child_key, child_node in children.items():
                matches = self._search_node(child_node, pattern[0:], path + child_key)
                matched.extend(matches)
            return matched

        if char not in children:
            return []

        return self._search_node(children[char], pattern[1:], path + char)

    def search(self, pattern: str) -> list[str]:
        if not pattern:
            return []

        matches = self._search_node(self._root, pattern, '')
        return sorted(set(matches))

    def clear(self) -> None:
        self._root[_Attribute.CHILDREN] = {}
