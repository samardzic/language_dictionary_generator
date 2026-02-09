import os

os.chdir("..\\resources\\serbian_dict\\resources_sr")
# os.chdir("..\\resources\\book_sources")
# file_name = "ciga_konj.txt"
# file_name = "book_na_drini_cuprija.txt"
# file_name = "book_necista_krv.txt"
# relative_path = os.getcwd()
# print(relative_path)
# n = os.listdir(os.getcwd())
# print(n)

for books in os.listdir(os.getcwd()):
    print(books)



# source_file = relative_path + "\\" + file_name