CREATE TABLE IF NOT EXISTS documents(
	doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
	text   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lexicon(
	term_id      INTEGER PRIMARY KEY AUTOINCREMENT,
	term         TEXT UNIQUE NOT NULL,
	is_protected BOOLEAN NOT NULL DEFAULT 0,
	doc_freq     INTEGER DEFAULT 0,
	col_freq     INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS inverted_index (
	term_id   INTEGER NOT NULL,
	doc_id    INTEGER NOT NULL,
	position  INTEGER NOT NULL,
	start_ofs INTEGER NOT NULL,
	end_ofs   INTEGER NOT NULL,
	PRIMARY KEY (term_id, doc_id, start_ofs, end_ofs),
	FOREIGN KEY (term_id) REFERENCES lexicon(term_id),
	FOREIGN KEY (doc_id)  REFERENCES documents(doc_id)
) WITHOUT ROWID;

CREATE TABLE IF NOT EXISTS lemmas (
	term_id  INTEGER PRIMARY KEY,
	lemma_id INTEGER NOT NULL,
	FOREIGN KEY (term_id)  REFERENCES lexicon (term_id) ON DELETE CASCADE,
	FOREIGN KEY (lemma_id) REFERENCES lexicon (term_id) ON DELETE CASCADE
);

