import os

# os.chdir("..\\resources\\serbian_dict\\resources_sr")
os.chdir("..\\resources\\book_sources")
# file_name = "ciga_konj.txt"
file_name = "book_tesla.txt"
relative_path = os.getcwd()
source_file = relative_path + "\\" + file_name


bad_chars = [",", ";", ":", "!", "?", "*", "„", '“', "\n", ".", "_"]
with open(source_file, "r", encoding="utf") as file_data:

    word_db = []
    word_counter = 0

    for line in file_data.readlines():
        clean_line = line
        for i in bad_chars:
            clean_line = clean_line.replace(i, "")

        word = clean_line.split(" ")
        for i in word:
            if i in word_db:
                continue
            else:
                word_db.append(i.lower())
                word_counter = word_counter + 1


    print(word_db)
    print(word_counter)
