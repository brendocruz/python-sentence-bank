from typing import TypedDict
from sentencebank.indexing.types import TermID

type VariationMap = dict[TermID, TermID]
type LemmaMap     = dict[TermID, list[TermID]]


class LemmatizerData(TypedDict):
    variations: VariationMap
    lemmas:     LemmaMap


class Lemmatizer:
    _data: LemmatizerData

    def __init__(self) -> None:
        self._data = {'variations': {}, 'lemmas': {}}
    
    def variation_count(self) -> int:
        return len(self._data['variations'])
    
    def lemma_count(self) -> int:
        return len(self._data['lemmas'])

    def clear(self) -> None:
        self._data['variations'] = {}
        self._data['lemmas']     = {}
    
    def remove_variation(self, variation_id: TermID) -> None:
        lemma = self._data['variations'].pop(variation_id, None)
        if lemma is None:
            return

        lemma_entry = self._data['lemmas'][lemma]
        lemma_entry.remove(variation_id)
        if len(lemma_entry) == 0:
            self._data['lemmas'].pop(lemma)

    def set_variation(self, variation_id: TermID, lemma_id: TermID) -> None:
        if variation_id in self._data['variations']:
            self.remove_variation(variation_id)

        self._data['variations'][variation_id] = lemma_id

        lemma_entry = self._data['lemmas'].get(lemma_id, None)
        if lemma_entry is None:
            self._data['lemmas'][lemma_id] = [variation_id]
            return
        lemma_entry.append(variation_id)

    def lemmatize(self, variation_id: TermID) -> TermID | None:
        return self._data['variations'].get(variation_id, None)

    def get_variations(self, lemma_id: TermID) -> list[TermID]:
        return self._data['lemmas'].get(lemma_id, [])

    def contains_variation(self, variation_id: TermID) -> bool:
        return variation_id in self._data['variations']

    def contains_lemma(self, lemma_id: TermID) -> bool:
        return lemma_id in self._data['lemmas']
