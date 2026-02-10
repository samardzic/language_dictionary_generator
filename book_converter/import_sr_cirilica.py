"""
Import script for sr_cirilica_262000.txt.

Reads Cyrillic words from the source file, transliterates each to Latin,
and inserts both into the words table with source tracking.
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "db" / "dictionary.db"
SOURCE_PATH = BASE_DIR / "language_sources" / "sr_cirilica_262000.txt"
SOURCE_NAME = "sr_cirilica_262000.txt"

# Cyrillic → Latin mapping (section 5.2 of app_requirements.md)
CYR_TO_LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
    "ђ": "đ", "е": "e", "ж": "ž", "з": "z", "и": "i",
    "ј": "j", "к": "k", "л": "l", "љ": "lj", "м": "m",
    "н": "n", "њ": "nj", "о": "o", "п": "p", "р": "r",
    "с": "s", "т": "t", "ћ": "ć", "у": "u", "ф": "f",
    "х": "h", "ц": "c", "ч": "č", "џ": "dž", "ш": "š",
    # Uppercase
    "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D",
    "Ђ": "Đ", "Е": "E", "Ж": "Ž", "З": "Z", "И": "I",
    "Ј": "J", "К": "K", "Л": "L", "Љ": "Lj", "М": "M",
    "Н": "N", "Њ": "Nj", "О": "O", "П": "P", "Р": "R",
    "С": "S", "Т": "T", "Ћ": "Ć", "У": "U", "Ф": "F",
    "Х": "H", "Ц": "C", "Ч": "Č", "Џ": "Dž", "Ш": "Š",
}


def transliterate_to_latin(word: str) -> str:
    """Transliterate a Cyrillic word to Latin script."""
    result = []
    for char in word:
        result.append(CYR_TO_LAT.get(char, char))
    return "".join(result)


def import_words():
    """Read .txt file and import words into the database."""
    if not SOURCE_PATH.exists():
        print(f"Error: Source file not found: {SOURCE_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    cursor = conn.cursor()

    # Register source file (one row, reused for all words)
    cursor.execute(
        "INSERT OR IGNORE INTO sources (file_name) VALUES (?)",
        (SOURCE_NAME,),
    )
    conn.commit()
    cursor.execute(
        "SELECT id FROM sources WHERE file_name = ?",
        (SOURCE_NAME,),
    )
    source_id = cursor.fetchone()[0]

    total = 0
    inserted = 0
    skipped = 0
    batch_size = 5000

    with open(SOURCE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            word_cyr = line.strip()
            if not word_cyr:
                continue

            total += 1
            word_lat = transliterate_to_latin(word_cyr)

            try:
                cursor.execute(
                    "INSERT INTO words (sr_cirilica, sr_latinica) VALUES (?, ?)",
                    (word_cyr, word_lat),
                )
                word_id = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO word_sources (word_id, source_id) VALUES (?, ?)",
                    (word_id, source_id),
                )
                inserted += 1
            except sqlite3.IntegrityError:
                skipped += 1

            if total % batch_size == 0:
                conn.commit()
                print(f"  Processed {total} words...")

    conn.commit()
    conn.close()

    print(f"\nImport complete:")
    print(f"  Source:   {SOURCE_NAME} (source_id={source_id})")
    print(f"  Total:    {total}")
    print(f"  Inserted: {inserted}")
    print(f"  Skipped:  {skipped} (duplicates)")


if __name__ == "__main__":
    import_words()
