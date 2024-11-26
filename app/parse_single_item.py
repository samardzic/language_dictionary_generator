import os

from app.parser_main import text_parser

os.chdir("..\\resources\\serbian_dict\\resources_sr")
# source_file = os.getcwd() + "\\book_na_drini_cuprija.txt"
source_file = os.getcwd() + "\\ciga_konj_short.txt"

data = text_parser(source_file)
print(data)
