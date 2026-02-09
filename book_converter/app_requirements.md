# Book Converter — Application Requirements

## 1. Project Goal

Build a dictionary database and conversion tool that:
1. Parses Serbian-language text files (books) and extracts unique words
2. Stores words in a SQLite database
3. Converts text between South Slavic language variants

### Supported Language Variants

| Key                      | Description                                  |
|--------------------------|----------------------------------------------|
| `sr_cirilica`            | Serbian Cyrillic (ћирилица)                  |
| `sr_latinica`            | Serbian Latin (latinica)                     |
| `sr_cirilica_extended`   | Serbian Cyrillic — extended dictionary       |
| `sr_latinica_extended`   | Serbian Latin — extended dictionary          |
| `hr_language`            | Croatian (hrvatski)                          |
| `hr_language_extended`   | Croatian — extended dictionary               |

### Conversion Pairs

- `sr_cirilica` ↔ `sr_latinica` — character-level transliteration
- `hr_language` ↔ `sr_cirilica` — vocabulary mapping + transliteration

Any variant should be convertible to any other variant.

---

## 2. Input Sources

- Plain text files (`.txt`) located in `resources/serbian_dict/resources_sr/` (old and new books)
- Additional book sources in `resources/book_sources/`
- Files are UTF-8 encoded, primarily in Serbian Cyrillic

### Available Sources

| Directory                                        | Content                                       |
|--------------------------------------------------|-----------------------------------------------|
| `resources/serbian_dict/resources_sr/old_books/` | Classic Serbian literature (Cyrillic)         |
| `resources/serbian_dict/resources_sr/new_books/` | Modern Serbian literature (Cyrillic)          |
| `resources/book_sources/`                        | Mixed-language book texts                     |
| `resources/serbian_dict/openOffice_dict/`.       | Hunspell dictionary (reference data)          |

---

## 3. Database Design

**Engine:** SQLite

### Tables

#### `words` — Master Word Table

| Column                 | Type    | Description                                          |
|------------------------|---------|------------------------------------------------------|
| `id`                   | INTEGER | Primary key, autoincrement                           |
| `sr_cirilica`          | TEXT    | Word in Serbian Cyrillic (NOT NULL)                  |
| `sr_latinica`          | TEXT    | Word in Serbian Latin (NOT NULL)                     |
| `sr_cirilica_extended` | TEXT    | Word in Serbian Cyrillic — extended dictionary       |
| `sr_latinica_extended` | TEXT    | Word in Serbian Latin — extended dictionary          |
| `hr_language`          | TEXT    | Croatian equivalent (NULL if same as sr_latinica)    |
| `hr_language_extended` | TEXT    | Croatian — extended dictionary                       |

#### `sources` — Word Source Tracking

| Column      | Type    | Description                               |
|-------------|---------|-------------------------------------------|
| `id`        | INTEGER | Primary key, autoincrement                |
| `word_id`   | INTEGER | Foreign key → `words.id`                  |
| `file_name` | TEXT    | Source file the word was extracted from    |

### Indexes

- `UNIQUE INDEX` on `words.sr_latinica` — primary key for dedup (Phase 1 seed language)
- `UNIQUE INDEX` on `words.sr_cirilica` — prevent duplicate Cyrillic entries
- `UNIQUE INDEX` on `words.sr_latinica_extended` — dedup for extended Latin entries
- `UNIQUE INDEX` on `words.sr_cirilica_extended` — dedup for extended Cyrillic entries
- `UNIQUE INDEX` on `words.hr_language` — prevent duplicate Croatian entries
- `UNIQUE INDEX` on `words.hr_language_extended` — dedup for extended Croatian entries
- `INDEX` on `sources.word_id` — fast join to word sources

---

## 4. Implementation Phases

### Phase 1 — Seed the Dictionary

**Goal:** Build a large `sr_latinica` dictionary and derive `sr_cirilica` from it.

1. Parse all available source text files and extract unique words
2. Populate the `sr_latinica` column as the primary entry for each word
3. Auto-generate the `sr_cirilica` column by applying Latin → Cyrillic transliteration
4. Result: a database where every row has both `sr_latinica` and `sr_cirilica` filled

### Phase 2 — Incremental Import

**Goal:** Grow the dictionary over time by importing new word lists without creating duplicates.

1. Accept an input word list (file or in-memory list)
2. For each word, check if it already exists in the database:
   - Look up against `sr_latinica` column
   - Look up against `sr_cirilica` column
3. If the word exists in either column → **skip**
4. If the word is new → transliterate to produce the other variant, then **insert** both columns
5. Log a summary: words added vs. words skipped

---

## 5. Core Features

### 5.1 Text Parsing

- Read `.txt` files and extract unique words
- Strip punctuation and special characters
- Normalize to lowercase
- Skip numeric-only tokens
- Deduplicate across multiple source files

### 5.2 Cyrillic ↔ Latin Transliteration

Rule-based character mapping:

| Cyrillic | Latin | Cyrillic | Latin |
|----------|-------|----------|-------|
| а → a    |       | п → p    |       |
| б → b    |       | р → r    |       |
| в → v    |       | с → s    |       |
| г → g    |       | т → t    |       |
| д → d    |       | у → u    |       |
| ђ → đ    |       | ф → f    |       |
| е → e    |       | х → h    |       |
| ж → ž    |       | ц → c    |       |
| з → z    |       | ч → č    |       |
| и → i    |       | џ → dž   |       |
| ј → j    |       | ш → š    |       |
| к → k    |       |          |       |
| л → l    |       | љ → lj   |       |
| м → m    |       | њ → nj   |       |
| н → n    |       |          |       |
| о → o    |       |          |       |

Transliteration must be bidirectional (Latin → Cyrillic requires digraph handling: `lj` → `љ`, `nj` → `њ`, `dž` → `џ`).

### 5.3 Vocabulary Mapping (Croatian)

For words that differ between variants, maintain explicit mappings. Examples:

| sr_cirilica | sr_latinica | sr_cirilica_extended | sr_latinica_extended | hr_language | hr_language_extended |
|-------------|-------------|----------------------|----------------------|-------------|----------------------|
| хлеб        | hleb        | хлеб                 | hleb                 | kruh        | kruh                 |
| ваздух      | vazduh      | ваздух               | vazduh               | zrak        | zrak                 |
| воз         | voz         | воз                  | voz                  | vlak        | vlak                 |

Words that are identical across variants only need the `sr_cirilica` and `sr_latinica` columns populated; `hr_language` and the extended columns remain `NULL` to indicate equivalence with `sr_latinica`.

### 5.4 Text Conversion

Given input text and a target language variant, convert the full text:
1. Tokenize input text (preserve punctuation and whitespace)
2. Look up each word in the database
3. Apply transliteration (for Cyrillic ↔ Latin)
4. Apply vocabulary substitution (for Croatian)
5. Reconstruct the converted text preserving original formatting

---

## 6. Technical Requirements

- **Language:** Python 3.13+
- **Database:** SQLite3 (stdlib `sqlite3` module)
- **No external dependencies** for core functionality
- **Project structure:** follows MVC pattern per CLAUDE.md guidelines
- **Entry point:** `book_converter/converter.py`

---

## 7. Future Considerations

- Import words from Hunspell dictionaries (`openOffice_dict/`) as additional vocabulary source
- Bulk text file conversion (batch mode)
- Export converted text to file
- CLI interface for interactive conversion
- Support for additional South Slavic variants (Bosnian, Montenegrin)