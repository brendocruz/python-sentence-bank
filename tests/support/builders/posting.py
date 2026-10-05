from sentencebank.indexing.types import DocID, Posting


class PostingTestBuilder:

    def build(self, doc_id: DocID, position: int, start: int, end: int) -> Posting:
        return Posting(doc_id=doc_id, position=position, start=start, end=end)
