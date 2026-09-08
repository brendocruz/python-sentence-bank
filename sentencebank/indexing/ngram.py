type TermList  = list[str]
type IndexData = dict[str, TermList]


class NgramIndex:
    _order:   int
    _entries: dict[str, TermList]

    def __init__(self, entries: IndexData | None = None, *, order: int = 3) -> None:
        self._entries = entries or {}
        self._order   = order

    def _generate_ngrams(self, term) -> list[str]:
        if term == '':
            return []

        ngrams: list[str] = []
        anchored = f'${term}$'
        end      = len(anchored) - self._order + 1
        for index in range(0, end):
            ngram = anchored[index:index+self._order]
            ngrams.append(ngram)
        return ngrams
        
    def add_term(self, term: str) -> None:
        ngrams = self._generate_ngrams(term)

        for ngram in ngrams:
            entry = self._entries.get(ngram, None)
            if entry is None:
                self._entries[ngram] = [term]
                continue
            if term in entry:
                continue
            entry.append(term)

    def remove_term(self, term: str) -> None:
        ngrams = self._generate_ngrams(term)

        for ngram in ngrams:
            entry = self._entries.get(ngram, None)
            if entry is None:
                continue
            if term not in entry:
                continue
            entry.remove(term)

            if len(entry) == 0:
                self._entries.pop(ngram)

    def get_terms(self, ngram: str) -> list[str]:
        return list(self._entries.get(ngram, []))

    def contains(self, ngram: str) -> bool:
        return ngram in self._entries

    def size(self) -> int:
        return len(self._entries)

    def clear(self) -> None:
        self._entries = {}
