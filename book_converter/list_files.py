# 1. ToDo: open file sr_cirilica_262000.txt as file
# 2. ToDo: iterate through "file" and show first 20 words

from pathlib import Path

SOURCE_PATH = Path(__file__).parent / "language_sources" / "sr_cirilica_262000.txt"


CYR_TO_LAT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d",
    "ђ": "đ", "е": "e", "ж": "ž", "з": "z", "и": "i",
    "ј": "j", "к": "k", "л": "l", "љ": "lj", "м": "m",
    "н": "n", "њ": "nj", "о": "o", "п": "p", "р": "r",
    "с": "s", "т": "t", "ћ": "ć", "у": "u", "ф": "f",
    "х": "h", "ц": "c", "ч": "č", "џ": "dž", "ш": "š",
    "А": "A", "Б": "B", "В": "V", "Г": "G", "Д": "D",
    "Ђ": "Đ", "Е": "E", "Ж": "Ž", "З": "Z", "И": "I",
    "Ј": "J", "К": "K", "Л": "L", "Љ": "Lj", "М": "M",
    "Н": "N", "Њ": "Nj", "О": "O", "П": "P", "Р": "R",
    "С": "S", "Т": "T", "Ћ": "Ć", "У": "U", "Ф": "F",
    "Х": "H", "Ц": "C", "Ч": "Č", "Џ": "Dž", "Ш": "Š",
}

def cirilic_to_latin(word):
    result = ""
    for c in word:
        result += CYR_TO_LAT.get(c, c)
    return result


with open(SOURCE_PATH, "r", encoding="utf-8") as file:
    for i, line in enumerate(file):
        if i >= 20:
            break
        cir = line.strip()
        lat = cirilic_to_latin(cir)
        print(f"{cir} -> {lat}")


# i=1
# with open(SOURCE_PATH, "r", encoding="utf-8") as file:
#     for line in file:
#         print(f"--- {line}")
#         i += 1
#         print(i)






# # Demo: convert the first 20 words
# print("\n--- Cyrillic → Latin ---")
# with open(SOURCE_PATH, "r", encoding="utf-8") as file:
#     for i, line in enumerate(file):
#         if i >= 20:
#             break
#         word = line.strip()
#         print(f"{i + 1}. {word} → {cirilic_to_latin(word)}")