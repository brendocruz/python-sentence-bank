type VariationMap = dict[str, str]
type LemmaMap     = dict[str, list[str]]

class Lemmatizer:
    _variations: VariationMap
    _lemmas:     LemmaMap

    def __init__(self, variations: VariationMap | None = None,
                 lemmas: LemmaMap | None = None) -> None:
        self._variations =  variations or {}
        self._lemmas     = lemmas or {}
    
    def variation_count(self) -> int:
        return len(self._variations)
    
    def lemma_count(self) -> int:
        return len(self._lemmas)

    def clear(self) -> None:
        self._variations = {}
        self._lemmas     = {}
    
    def remove_variation(self, variation) -> None:
        lemma = self._variations.pop(variation, None)
        if lemma is None:
            return

        lemma_entry = self._lemmas[lemma]
        lemma_entry.remove(variation)
        if len(lemma_entry) == 0:
            self._lemmas.pop(lemma)

    def set_variation(self, variation: str, lemma: str) -> None:
        if variation in self._variations:
            self.remove_variation(variation)

        self._variations[variation] = lemma

        lemma_entry = self._lemmas.get(lemma, None)
        if lemma_entry is None:
            self._lemmas[lemma] = [variation]
            return
        lemma_entry.append(variation)

    def lemmatize(self, variation: str) -> str:
        return self._variations.get(variation, '')

    def get_variations(self, lemma: str) -> list[str]:
        return self._lemmas.get(lemma, [])

    def contains_variation(self, variation: str) -> bool:
        return variation in self._variations

    def contains_lemma(self, lemma: str) -> bool:
        return lemma in self._lemmas
