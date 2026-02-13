import os


def text_parser():
    # os.chdir("..\\resources\\serbian_dict\\resources_sr\\old_books")
    # os.chdir("..\\resources\\book_sources")
    # file_name = "ciga_konj.txt"
    # file_name = "book_na_drini_cuprija.txt"
    # file_name = "book_necista_krv.txt"
    # relative_path = os.getcwd()

    # os.chdir("..\\resources\\serbian_dict\\resources_sr")
    # relative_path = os.getcwd()
    # print(relative_path)
    # all_words = []
    #


    # os.chdir("..\\resources\\book_sources")
    os.chdir("/home/nenad/Build/language_dictionary_generator/book_converter/book_parser/stories")

    relative_path = os.getcwd()  # /home/ime/Build/python_sandbox
    print("Relative path is: " + relative_path)

    # source_file = relative_path + "\\book_hunger_games_short.txt"
    source_file = relative_path + "/cro_renato.txt"
    print("Sources: " + source_file)
    word_db = []
    for book in os.listdir(os.getcwd()):
        print(book)
        # book_name = os.getcwd() + "/" + book





        # book_name = os.getcwd() + "\\" + book



        bad_chars = [",", ";", "&", ":", "!", "?", "*", "'", "„", '“', "\n", "_", "«", "»", "(", ")", "...", "..", ".", '"', "-"]
        with open(book_name, "r", encoding="utf") as file_data:

            # word_db = []
            word_counter = 0

            for line in file_data.readlines():
                clean_line = line.lower()
                for i in bad_chars:
                    clean_line = clean_line.replace(i, "")

                word = clean_line.split(" ")
                for i in word:
                    if i.isdigit():
                        continue
                    elif i in word_db:
                        continue
                    else:
                        word_db.append(i)
                        word_counter = word_counter + 1

            # return word_db
    word_db.sort()
    # print(word_db)
    # print(word_counter)
    output_file = os.getcwd() + "/dict_rs.txt"


    # Save extracted text to file
    output_file = Path(source_file).with_suffix('.data')
    output_file.write_text(text, encoding='utf-8')
    print(f"\n✓ Text saved to: {output_file}")
    print(f"  File size: {output_file.stat().st_size:,} bytes")


    with open(output_file, "w", encoding="utf") as file_data:
        output_data = str(word_db)
        final_data = output_data.replace("', '", "\n")
        file_data.write(final_data)

text_parser()

