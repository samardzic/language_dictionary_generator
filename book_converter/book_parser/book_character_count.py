import os
import re
import sys
from pathlib import Path

# Add parent directory to path to import converter
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from converter import PDFConverter


# os.chdir("..\\resources\\book_sources")
os.chdir("/home/nenad/Build/language_dictionary_generator/book_converter/book_parser/stories")

relative_path = os.getcwd()  # /home/ime/Build/python_sandbox
print("Relative path is: " + relative_path)

# source_file = relative_path + "\\book_hunger_games_short.txt"
source_file = relative_path + "/cro_renato.pdf"
print("Sources: " + source_file)



# Create PDFConverter instance and convert PDF to text
converter = PDFConverter()
text = converter.convert_pdf_to_text(Path(source_file))

print(f"\nExtracted text length: {len(text)} characters")
# print(f"First 500 characters:\n{text[:500]}")
# print("\n" + "="*50)

# Save extracted text to file
output_file = Path(source_file).with_suffix('.txt')
output_file.write_text(text, encoding='utf-8')
print(f"\n✓ Text saved to: {output_file}")
print(f"  File size: {output_file.stat().st_size:,} bytes")



# Opens the source file and stores it as a FILE_INPUT
with open(output_file, encoding='utf-8') as file_input:
    my_data = file_input.read()  # Reads from the source file (FILE_INPUT)

# Regex to remove special characters but KEEP Serbian/Croatian letters
# Keeps: a-z, A-Z, 0-9, and Serbian/Croatian special characters (č, ć, š, ž, đ)
regex_list = re.sub(r"[^a-zA-Z0-9čćšžđČĆŠŽĐ]", " ", my_data)

# While loop to replace multiple-spaces with single-spaces
while '  ' in regex_list:
    regex_list = regex_list.replace('  ', ' ')

# print(regex_list)



 

# # # Opens the source file and stores it as a FILE_INPUT
# with open(source_file) as file_input:
#     my_data = file_input.read()  # Reads from the source file (FILE_INPUT)

# # Regex to remove special characters from the source file
# regex_list = re.sub(r"[^a-zA-Z0-9]", " ", my_data)

# # While loop to replace multiple-spaces with single-spaces
# while '  ' in regex_list:
#     regex_list = regex_list.replace('  ', ' ')

# print(regex_list)


words_number = 0

for c in my_data:
    if my_data != " ":
        words_number += 1
        # print(words_number)

print(words_number)
