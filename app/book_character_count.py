import os
import re


relative_path = os.getcwd()  # /home/ime/Build/python_sandbox
print("Relative path is: " + relative_path)

source_file = relative_path + ".\\resources\\book_sources\\book_hunger_games_short.txt"
print("Sources: " + source_file)

# Opens the source file and stores it as a FILE_INPUT
with open(source_file) as file_input:
    my_data = file_input.read()  # Reads from the source file (FILE_INPUT)

# Regex to remove special characters from the source file
regex_list = re.sub(r"[^a-zA-Z0-9]", " ", my_data)

# While loop to replace multiple-spaces with single-spaces
while '  ' in regex_list:
    regex_list = regex_list.replace('  ', ' ')

print(regex_list)


words_number = 0

for c in my_data:
    if my_data != " ":
        # print("This is my data:", my_data)
        words_number += 1
        print(words_number)

print(words_number)
