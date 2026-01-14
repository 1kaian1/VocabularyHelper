import os
import pickle
import random
import sys
import _thread
import time
import json

print("Vocabulary 1.0")


class User:

    def __init__(self):

        if not os.path.exists("PythonVocabulary"):
            os.mkdir("PythonVocabulary")
        if not os.path.exists("PythonVocabulary/abackup"):
            os.mkdir("PythonVocabulary/abackup")

        self.language = None
        self.language_data = None
        self.terminate_autosave = False
        self.destination = None
        self.learning_time = None
        self.swap = True
        self.raiseup = True

        self.menu()

    def menu(self):
        self.destination = "menu"

        """Offers basic actions for user."""

        print("-" * 10 + "\nx - New database")

        directory_files = os.listdir("PythonVocabulary")

        x = 1
        for file in directory_files:
            file_name = file.split(".")
            if file_name[0] != "abackup":
                print(f"{x} - {file_name[0]}")
                x += 1

        action = self.input("* - Delete language\n/ - Terminate program\n>>>", False)

        try:

            if action == "x":
                self.new_language()
            elif action == "/":
                sys.exit()
            elif action == "*":
                self.delete_language()
            elif os.path.exists(f"PythonVocabulary/{directory_files[int(action)]}"):
                self.language = directory_files[int(action)]
                self.initiate_language()

        except Exception as exc:
            self.print(f"[{exc.__class__.__name__}: {exc.__class__.__doc__}]", "red")
            User.__dict__[self.destination](self)

    def delete_language(self):
        self.destination = "delete_language"

        directory_files = os.listdir("PythonVocabulary")

        id = self.input("Select language: (format \"1\") (\"/\" to quit)\n>>>")

        if id == "/":
            pass
        else:
            os.remove(f"PythonVocabulary/{directory_files[int(id)]}")

        self.menu()

    def new_language(self):

        name = self.input("Enter the name: (\"/\" to quit)\n>>>")
        name += ".json"

        if os.path.exists(f"PythonVocabulary/{name}"):
            self.print("[FAILED: Language already exists.]", "red")
            self.new_language()
        elif name == "/":
            self.menu()
        else:
            self.write_file(name, ([], [], [], []))
            self.language = name
            self.initiate_language()

    def initiate_language(self):
        self.destination = "initiate_language"

        if self.language_data is None:
            self.language_data = self.read_file(self.language)
            _thread.start_new_thread(self.autosave, ())

        self.print_database()

        task = self.input(f"1 - Start exercise\n2 - Enter new words\n3 - Delete words\n/ - Quit\n>>>", False)

        if task == "/":
            self.terminate_autosave = True
            self.write_file(self.language, self.language_data)
            self.language_data = None
            self.menu()
        elif task == "1" and self.language_data == ([], [], [], []):
            self.print("[FAILED: No words.]", "red")
            self.initiate_language()
        elif task == "1" and self.language_data != ([], [], [], []):
            print("\n"*50)
            self.drill()
        elif task == "2":
            self.new_word()
        elif task == "3":
            self.delete_word()
        else:
            self.print("[FAILED: Task doesn't exist.]", "red")
            self.initiate_language()

    def new_word(self):
        self.destination = "new_word"

        filename = self.input("Enter filename with words (\"/\" to quit):\n>>> ")

        if filename == "/":
            return

        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            self.print("[FAILED: File not found.]", "red")
            return

        log_filename = "invalid_lines.txt"

        for line_number, line in enumerate(lines, start=1):
            original_line = line.rstrip("\n")
            line = line.strip()

            if not line:
                continue

            # kontrola formátu
            if " - " not in line:
                with open(log_filename, "a", encoding="utf-8") as log:
                    log.write(f"{filename}:{line_number}: {original_line}\n")
                continue

            origin, translations = line.split(" - ", 1)

            # rozpoznání členu
            if origin.startswith("der "):
                article = "r"
            elif origin.startswith("die "):
                article = "e"
            elif origin.startswith("das "):
                article = "s"
            elif origin.startswith("Die "):
                article = "p"
            else:
                article = "x"

            translation = translations.strip()

            if origin in self.language_data[0]:
                continue

            self.language_data[0].append(origin)
            self.language_data[1].append(translation)
            self.language_data[2].append(15)
            self.language_data[3].append(article)

        self.initiate_language()

    def new_words(self):
        self.destination = "new_word"

        go_on = True
        while go_on:

            word = self.input("Enter new word: (format \"ahoj:hi\") (\"/\" to quit)\n>>>")

            if word == "/":
                go_on = False
            else:

                origin, translation = word.split(":")

                if origin.startswith("der "):
                    article = "r"
                elif origin.startswith("die "):
                    article = "e"
                elif origin.startswith("das "):
                    article = "s"
                elif origin.startswith("Die "):
                    article = "p"
                else:
                    article = "-"

                if (origin in self.language_data[0]) or (translation in self.language_data[1]):
                    self.print("[FAILED: Word already exists.]", "red")
                else:
                    self.language_data[0].append(origin)
                    self.language_data[1].append(translation)
                    self.language_data[2].append(15)
                    self.language_data[3].append(article)



        self.initiate_language()

    def print_database(self):

        print("-" * 150)

        primary_list, secondary_list, tertiary_list, quartile_list = self.sort_database()

        x = 0
        while x < len(primary_list):

            primary_word = primary_list[x]
            secondary_word = secondary_list[x]
            tertiary_word = tertiary_list[x]
            quartile_word = quartile_list[x]

            if len(primary_word) < 50:
                primary_word = self.add_gap(primary_word, 50)
            if len(secondary_word) < 50:
                secondary_word = self.add_gap(secondary_word, 50)
            if len(str(tertiary_word)) < 5:
                tertiary_word = self.add_gap(str(tertiary_word), 5)
            if len(str(x)) < 5:
                xp = self.add_gap(str(x), 5)

            print(f"No.{xp} | {primary_word} | {secondary_word} | {tertiary_word} | {quartile_word}")

            x += 1

        print("-" * 150)

    def sort_database(self):

        unsorted_list = self.language_data[0]
        sorted_list = sorted(unsorted_list, key=str.lower)

        pst_list = self.language_data[1]  # pst_list: pair-sorted translation list: needs to be sorted by pairs and
        # contains translations
        pst_list_clone = pst_list[:]

        psp_list = self.language_data[2]  # psp_list: pair-sorted probability list: needs to be sorted by pairs and
        # contains probabilities
        psp_list_clone = psp_list[:]

        psc_list = self.language_data[3]  # psc_list: pair-sorted color list: needs to be sorted by pairs and
        # contains colors
        psc_list_clone = psc_list[:]

        for word in sorted_list:

            old_position = unsorted_list.index(word)
            new_position = sorted_list.index(word)

            paired_translation = pst_list[old_position]
            pst_list_clone[new_position] = paired_translation

            paired_probability = psp_list[old_position]
            psp_list_clone[new_position] = paired_probability

            paired_color = psc_list[old_position]
            psc_list_clone[new_position] = paired_color

        self.language_data = (sorted_list, pst_list_clone, psp_list_clone, psc_list_clone)

        return sorted_list, pst_list_clone, psp_list_clone, psc_list_clone

    def delete_word(self):
        self.destination = "delete_word"

        task = self.input("Enter Nos (format 1,2,3) (\"/\" to quit)\n>>>")
        
        if task == "/":
            self.initiate_language()

        task_confirmed = ""
        for a in task:
            if a != " ":
                task_confirmed += a

        task_confirmed = task_confirmed.split(",")

        for a in task_confirmed:
            self.language_data[0][int(a)] = "/"
            self.language_data[1][int(a)] = "/"
            self.language_data[2][int(a)] = "/"
            self.language_data[3][int(a)] = "/"

        list1 = self.item_deletion(self.language_data[0])
        list2 = self.item_deletion(self.language_data[1])
        list3 = self.item_deletion(self.language_data[2])
        list4 = self.item_deletion(self.language_data[3])

        self.language_data = (list1, list2, list3, list4)

        self.initiate_language()

    def drill(self):

        self.learning_time = time.time()

        go_on = True
        while go_on:

            id, id2 = 1, 0

            word = random.choices(self.language_data[id], self.language_data[2], k=1)[0]

            index = self.language_data[id].index(word)

            correct_answer = self.language_data[id2][index]

            print(10*"-", "\nTranslate: ", end="")
            self.print(word, color=None, end=False, indentation=False)
            print(f" | index: {self.language_data[2][index]} (\"/\" to quit, \"-\" for swapping, \"!\" for addition, \"l\" for \"learned\")")
            user_answer = self.input(">>>")

            if correct_answer == user_answer:
                self.print("Correct!", "green")

                if self.language_data[2][index] > 1:
                    self.language_data[2][index] -= 1

            elif user_answer == "/":
                self.learning_time = round(time.time()-self.learning_time)
                self.print(f"Learning time: {self.learning_time//60}:{self.learning_time%60}")
                self.initiate_language()

            elif user_answer == "-":
                if self.swap:
                    self.swap = False
                    self.print("[Swap disabled.]")
                else:
                    self.swap = True
                    self.print("[Swap enabled.]")

            elif user_answer == "!":
                if self.raiseup:
                    self.raiseup = False
                    self.print("[Addition disabled.]")
                else:
                    self.raiseup = True
                    self.print("[Addition enabled.]")

            elif user_answer == "l":
                self.language_data[2][index] = 1
                self.print("[Spawn probability set to 1.]")

            elif self.raiseup:
                self.print(f"Wrong. Correct answer: {self.language_data[id2][index]}", "red")

                if self.language_data[2][index] < 30:
                    self.language_data[2][index] += 1

            else:
                self.print(f"Correct answer: {self.language_data[id2][index]}", "red")

    def autosave(self):
        """Threaded function for autosave."""

        oldtime = time.time()

        while not self.terminate_autosave:

            if int(oldtime) + 2 == int(time.time()):

                self.write_file(self.language, self.language_data)

                oldtime = time.time()

    def input(self, text, indentation=True):

        try:

            if indentation is False:
                answer = input(text)
            else:
                answer = input("-" * 10 + "\n" + text)
            return answer

        except KeyboardInterrupt:
            self.terminate_autosave = True
            self.write_file(self.language, self.language_data)
            sys.exit()

    @staticmethod
    def print(text, color=None, end=True, indentation=True) -> None:

        if color == "green" or color == "s":
            color = "\033[92m{}\033[00m"
        elif color == "red" or color == "e":
            color = "\033[91m{}\033[00m"
        elif color == "r":
            color = "\033[94m{}\033[00m"
        elif color == "p":
            color = "\033[93m{}\033[00m"
        else:
            color = "\033[99m{}\033[00m"

        if indentation:
            print("----------")

        if end is False:
            print(color.format(text), end="")
        else:
            print(color.format(text))

    @staticmethod
    def item_deletion(register) -> list:

        while "/" in register:

            index = register.index("/")
            del register[index]

        return register

    @staticmethod
    def add_gap(content, gap) -> str:

        while len(content) < gap:

            content += " "

        return content

    @staticmethod
    def read_file(filename) -> tuple:
        words = []
        translations = []
        numbers = []
        flags = []

        with open(f"PythonVocabulary/{filename}", "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    # ahoj - hello | 15 | x
                    left, right = line.split(" - ", 1)
                    translation, number, flag = [part.strip() for part in right.split("|", 2)]

                    words.append(left.strip())
                    translations.append(translation)
                    numbers.append(int(number))
                    flags.append(flag)

                except ValueError:
                    raise ValueError(
                        f"Invalid format on line {line_number}: {line}"
                    )

        return words, translations, numbers, flags

    #@staticmethod
    #def read_file(filename) -> tuple:
    #    with open(f"PythonVocabulary/{filename}", "r", encoding="utf-8") as file:
    #        data = json.load(file)
    #    return data

    @staticmethod
    def write_file(filename, content) -> None:
        words, translations, numbers, flags = content

        # hlavní soubor
        with open(f"PythonVocabulary/{filename}", "w", encoding="utf-8") as file:
            for w, t, n, f in zip(words, translations, numbers, flags):
                file.write(f"{w} - {t} | {n} | {f}\n")

        # backup
        filename = filename.removesuffix(".txt")
        with open(f"PythonVocabulary/abackup/{filename}.backup", "w", encoding="utf-8") as file:
            for w, t, n, f in zip(words, translations, numbers, flags):
                file.write(f"{w} - {t}|{n}|{f}\n")

    #@staticmethod
    #def write_file(filename, content) -> None:
    #    with open(f"PythonVocabulary/{filename}", "w", encoding="utf-8") as file:
    #        json.dump(content, file, ensure_ascii=False, indent=2)
#
    #    filename = filename.removesuffix(".json")
    #    with open(f"PythonVocabulary/abackup/{filename}.backup", "w", encoding="utf-8") as file:
    #        json.dump(content, file, ensure_ascii=False, indent=2)

    #@staticmethod
    #def read_file(filename) -> tuple:
#
    #    with open(f"PythonVocabulary/{filename}", "rb") as file:
    #        data = pickle.load(file)
#
    #    return data
#
    #@staticmethod
    #def write_file(filename, content) -> None:
#
    #    with open(f"PythonVocabulary/{filename}", "wb") as file:
    #        pickle.dump(content, file)
#
    #    filename = filename.removesuffix(".vcblr")
    #    with open(f"PythonVocabulary/abackup/{filename}.backup", "wb") as file:
    #        pickle.dump(content, file)
#

User()
