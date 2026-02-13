
import os
import re


relative_path = os.getcwd()  # /home/ime/Build/python_sandbox
os.chdir(".\\resources\\book_sources")
source_file = relative_path + ".\\resources\\book_sources\\book_hunger_games_mini.txt"
print("Sources: " + source_file)

# Opens the source file and stores it as a FILE_INPUT
with open(source_file) as file_input:
    my_data = file_input.read() # Reads from the source file (FILE_INPUT)


# Regex to remove special characters from the source file
regex_list = re.sub(r"[^a-zA-Z0-9]"," ", my_data)


# While loop to replace multiple-spaces with single-spaces
while '  ' in regex_list:
    regex_list = regex_list.replace('  ', ' ')


# Splits the content read from the source file by " " (space char)
word_list = regex_list.split(' ') # splits the joined strings to new list


# Sorts the content of the WORD_LIST
word_list.sort()


# Returns the Count of unique words in the source file
word_count = [ii for n,ii in enumerate(word_list) if ii not in word_list[:n]]

for index, word_count in enumerate(word_count, start=1):
    print(index, word_count.lower())
