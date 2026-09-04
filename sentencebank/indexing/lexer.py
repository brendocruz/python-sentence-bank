from sentencebank.indexing.tokens import Token


class IndexingLexer:
    alphabet: str

    def __init__(self, alphabet: str):
        self.alphabet = alphabet

    def _is_word_char(self, char: str) -> bool:
        return char in self.alphabet

    def tokenize(self, text: str) -> list[Token]:
        tokens: list[Token] = []

        token_start: int
        token_end: int
        token_position = 0

        length = len(text)
        index  = 0

        while index < length:
            while index < length and not self._is_word_char(text[index]):
                index += 1
            token_start = index

            if index >= length:
                break

            while index < length and self._is_word_char(text[index]):
                index += 1
            token_end = index

            token_text = text[token_start:token_end]
            token = Token(text=token_text, position=token_position,
                          start=token_start, end=token_end)
            tokens.append(token)

            token_position += 1

        return tokens
