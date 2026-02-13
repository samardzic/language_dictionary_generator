import os

# Import from same directory (both files are in book_parser/)
from parser_main import text_parser


# os.chdir("..\\resources\\book_sources")
os.chdir("/home/nenad/Build/language_dictionary_generator/book_converter/book_parser/stories/")

relative_path = os.getcwd()  # /home/ime/Build/python_sandbox
print("Relative path is: " + relative_path)

# source_file = relative_path + "\\book_hunger_games_short.txt"
source_file = relative_path + "cro_renato.txt"
print("Sources: " + source_file)


# os.chdir("..\\resources\\serbian_dict\\resources_sr")
# # source_file = os.getcwd() + "\\book_na_drini_cuprija.txt"
# source_file = os.getcwd() + "\\ciga_konj_short.txt"

# data = text_parser(source_file)
# print(data)
