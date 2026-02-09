import os

from app.parser_main import text_parser

os.chdir("..\\resources\\serbian_dict\\resources_sr")
relative_path = os.getcwd()
print(relative_path)
all_words = []

for book in os.listdir(os.getcwd()):
    book_name = os.getcwd() + "\\" + book
    print(book_name)
    # print(os.getcwd() + "\\" + book)
    d = text_parser(book_name)
    s = 22
    all_words.append(text_parser(book_name))

    print(all_words)

