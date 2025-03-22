"""
Smart Typer v5.1

This script is a typing practice tool that generates random words based on various criteria
and tracks the user's typing performance. The program uses tkinter for the GUI, numpy for
random selection, and matplotlib for plotting performance metrics.

The script is organized into the following sections:
1. Imports and Global Variables: Importing necessary libraries and defining global variables.
2. Wordset Class: Handles word selection, filtering, and modification based on user input.
3. MainWindow Class: Inherits from Wordset and manages the GUI, user interactions, and performance tracking.
4. Utility Functions: Helper functions for creating GUI elements and handling events.
5. Main Function: Initializes and runs the tkinter main loop.
"""

import csv
import random
import statistics as stat
import time as tm
import tkinter as tk
from tkinter import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pynput.keyboard import Key, Controller

kb = Controller()


# Wordset Class: Handles word selection, filtering, and modification based on user input.
class Wordset:
    def __init__(self):
        # Load data from CSV files
        self.data = self.load_csv('Touch-Typing-Trainer-[GH]/data2_10kcut.csv')
        self.monogram = self.load_csv_as_dict('Touch-Typing-Trainer-[GH]/monogram.csv')
        self.bigram = self.load_csv_as_dict('Touch-Typing-Trainer-[GH]/bigram2.csv')
        self.trigram = self.load_csv_as_dict('Touch-Typing-Trainer-[GH]/trigram2.csv')
        self.action_record = self.load_csv('Touch-Typing-Trainer-[GH]/action_record.csv')

        # Initialize word selection parameters
        self.keylist = "a"
        self.keylistR = "a"
        self.keylistC = "A"
        self.keylistC_conv = "a"
        self.keylistN = "0"
        self.keylistP = ","
        self.keylistB = "("
        self.minsize = 1
        self.printline = ""
        self.R_monograms = []
        self.C_monograms = []
        self.N_monograms = []
        self.N_monograms_choice = []
        self.P_monograms = []
        self.B_monograms = []

    # CSV Loading Functions
    def load_csv(self, filename):
        with open(filename) as csvfile:
            return list(csv.reader(csvfile, delimiter=","))

    def load_csv_as_dict(self, filename):
        with open(filename) as csvfile:
            return {rows[0]: rows[1] for rows in csv.reader(csvfile, delimiter=",")}

    # Word Filtering Functions
    def isallowed(self, word):
        """Check if a word is allowed based on the current keylist and minsize."""
        if len(word) < self.minsize:
            return False
        return all(letter in self.keylistR for letter in word)

    def search_words(self):
        """Filter words from the dataset based on allowed criteria."""
        self.activelist = [line for line in self.data if self.isallowed(line[0])]

    def isallowedC(self, word):
        """Check if a word is allowed for capitalized words."""
        if len(word) < self.minsize or word[0] not in self.keylistC_conv:
            return False
        return all(letter in self.keylistR for letter in word[1:])

    def search_wordsC(self):
        """Filter words from the dataset for capitalized words."""
        self.activelistC = [line for line in self.data if self.isallowedC(line[0])]

    # Word Selection Functions
    def choose_regular(self):
        """Randomly choose a word from the active list based on frequency."""
        return np.random.choice(self.wordlist, size=1, p=self.freqlist)[0]

    def choose_capital(self):
        """Randomly choose a capitalized word from the active list."""
        return np.random.choice(self.wordlistC, size=1, p=self.freqlistC)[0].capitalize()

    def choose_number(self):
        """Generate a random number string based on allowed characters."""
        wordlen = random.randint(3, 7)
        select_word = ""
        for i in range(wordlen):
            char = np.random.choice(self.wordlistN, size=1, p=self.freqlistN)[0]
            select_word += self.validate_number_char(char, i, wordlen)
        return select_word

    def validate_number_char(self, char, i, wordlen):
        """Ensure the selected character is valid based on its position in the number."""
        if i == 0:
            while char in ".%":
                char = np.random.choice(self.wordlistN, size=1, p=self.freqlistN)[0]
        elif i == 1:
            while char in ".£$€%":
                char = np.random.choice(self.wordlistN, size=1, p=self.freqlistN)[0]
        elif i == wordlen - 1:
            while char in ".£$€":
                char = np.random.choice(self.wordlistN, size=1, p=self.freqlistN)[0]
        else:
            while char in "£$€%":
                char = np.random.choice(self.wordlistN, size=1, p=self.freqlistN)[0]
        return char

    # Word Modification Functions
    def modify_punc(self, word):
        """Add a random punctuation mark to the end of the word."""
        char = np.random.choice(self.wordlistP, size=1, p=self.freqlistP)[0]
        return word + char

    def modify_bracket(self, word):
        """Enclose the word in random brackets."""
        char = np.random.choice(self.wordlistB, size=1, p=self.freqlistB)[0]
        char2 = self.get_closing_bracket(char)
        return char + word + char2

    def get_closing_bracket(self, char):
        """Return the corresponding closing bracket for the given opening bracket."""
        return {
            '"': '"',
            '(': ')',
            '[': ']',
            '{': '}',
        }.get(char, '')

    # Word Selection and Modification Workflow
    def choosewords(self):
        """Select words based on the current settings and build the final word list."""
        self.search_words()
        self.search_wordsC()
        self.selected = []

        # Set up frequency selection for each case
        self.setup_frequency_lists()

        selected_length = 0
        while selected_length < 60:
            select_word = self.select_word_based_on_type()
            select_word = self.modify_word_based_on_type(select_word)
            if selected_length + len(select_word) <= 60:
                selected_length += len(select_word)
                self.selected.append(select_word)
            else:
                break

    def setup_frequency_lists(self):
        """Prepare frequency lists for different word types."""
        self.wordlist = [row[0] for row in self.activelist]
        self.freqlist = self.normalize_frequencies([int(row[6]) for row in self.activelist])

        self.wordlistC = [row[0] for row in self.activelistC]
        self.freqlistC = self.normalize_frequencies(
            [int(0.5 * float(row[6]) + 0.5 * float(self.monogram[row[0][0].capitalize()])) for row in self.activelistC]
        )

        self.wordlistN = [k for k, v in self.N_monograms]
        self.freqlistN = self.normalize_frequencies([int(float(v)) for k, v in self.N_monograms])

        self.wordlistP = [k for k, v in self.P_monograms]
        self.freqlistP = self.normalize_frequencies([int(float(v)) for k, v in self.P_monograms])

        self.wordlistB = [k for k, v in self.B_monograms]
        self.freqlistB = self.normalize_frequencies([int(float(v)) for k, v in self.B_monograms])

        self.setup_choose_matrix()

    def normalize_frequencies(self, freqlist):
        """Normalize a list of frequencies to sum to 1."""
        freqsum = sum(freqlist)
        return [n / freqsum for n in freqlist]

    def setup_choose_matrix(self):
        """Calculate mean scores for each word type and set up the selection matrix."""
        self.choose_matrix = {
            'R': stat.mean([v for k, v in self.R_monograms]) if self.R_monograms else 0,
            'C': stat.mean([v for k, v in self.C_monograms]) if self.C_monograms else 0,
            'N': stat.mean([v for k, v in self.N_monograms_choice]) if self.N_monograms_choice else 0,
            'P': stat.mean([v for k, v in self.P_monograms]) if self.P_monograms else 0,
            'B': stat.mean([v for k, v in self.B_monograms]) if self.B_monograms else 0,
        }

        self.wordlistM = [k for k, v in self.choose_matrix.items() if k in "RCN"]
        self.freqlistM = self.normalize_frequencies([int(float(v)) for k, v in self.choose_matrix.items() if k in "RCN"])

        self.wordlistM2 = [k for k, v in self.choose_matrix.items()]
        self.freqlistM2 = self.normalize_frequencies([int(float(v)) for k, v in self.choose_matrix.items()])

    def select_word_based_on_type(self):
        """Select a word based on the type (Regular, Capital, Number)."""
        while True:  # Keep selecting until a valid choice is made
            classtype = np.random.choice(self.wordlistM, size=1, p=self.freqlistM)[0]
            if classtype == "R":
                return self.choose_regular()
            elif classtype == "C":
                if self.wordlistC:  # Only pick capital words if available
                    return self.choose_capital()
            else:
                return self.choose_number()


    def modify_word_based_on_type(self, select_word):
        """Modify the selected word based on punctuation or bracket type."""
        classtype2 = np.random.choice(self.wordlistM2, size=1, p=self.freqlistM2)[0]
        if classtype2 == "P":
            return self.modify_punc(select_word)
        elif classtype2 == "B":
            return self.modify_bracket(select_word)
        return select_word

    def printselected(self):
        """Generate the final string of selected words."""
        self.choosewords()
        self.printline = " ".join(self.selected) + " "


# MainWindow Class: Manages the GUI, user interactions, and performance tracking.
class MainWindow(Wordset):
    font = ("Calibri", 28)  # Define the font attribute here
    total_letters = 0
    start_time = tm.time()
    letterpos = 0
    current_pos = 0
    width = 70
    w_freq = 1
    w_monogram = 1
    w_bigram = 1
    w_trigram = 1
    score = 0
    penalty = False
    error_list = []
    bcksp = False
    original_letters = "aoris etngmqwyfuplbjxcdvhzkAORISETNGMQWYFUPLBJXCDVHZK"

    def __init__(self, master):
        super().__init__()
        self.cleanmonogram = []
        self.cleanbigram = []
        self.cleantrigram = []
        self.frame = Frame(master)
        self.create_gui(master)
        self.load_records()
        self.frame.pack()
        self.set_space(target=800)
        self.action()

    # GUI Creation Functions
    def create_gui(self, master):
        """Create and arrange GUI elements."""
        gui_row = 0
        self.lbl_letters = self.create_label("Letters:", gui_row, 0)
        self.text_letters = self.create_textfield(self.original_letters, gui_row, 1)
        
        # New tag configurations for letter list colours
        self.text_letters.tag_config("green", foreground="green")
        self.text_letters.tag_config("orange", foreground="orange")
        self.text_letters.tag_config("red", foreground="red")
        self.text_letters.tag_config("purple", foreground="purple")
        
        gui_row += 1
        self.lbl_symbols = self.create_label("Symbols:", gui_row, 0)
        self.ent_symbols = self.create_entry(r""",.'"(;:!?/-0123456789%£$€&^*=_+<>@[{#~\| """, 70, gui_row, 1)
        
        gui_row += 1
        self.lbl_untouched = self.create_label("Untouched", gui_row, 0)
        self.lbl_untouched2 = self.create_label("", gui_row, 1)
        
        gui_row += 1
        self.lbl_score = self.create_label("Score (T<400)", gui_row, 0)
        self.lbl_score2 = self.create_label("", gui_row, 1)
        
        gui_row += 1
        self.lbl_words = self.create_label("Generated words:", gui_row, 0)
        self.txt_words = self.create_textfield("", gui_row, 1)
        self.txt_words.tag_config("correct", background="green")
        self.txt_words.tag_config("error", background="red")
        self.txt_words.tag_config("part", background="orange")
        
        gui_row += 1
        self.lbl_type = self.create_label("Type here:", gui_row, 0)
        self.ent_type = self.create_entry("", 70, gui_row, 1)
        self.ent_type.config(background="yellow")
        self.lbl_wpm2 = self.create_label("?? WPM", gui_row, 2)
        
        gui_row += 1
        self.gui_row = gui_row
        gui_row += 1
        self.lbl_placeholder = self.create_label("Copyright Marij Qureshi 2021", gui_row + 1, 1)
        
        # Set bindings
        master.bind('<Return>', self.action)
        master.bind('<Control-r>', self.reset)
        master.bind('<Control-BackSpace>', self.entry_ctrl_bs)
        master.bind('<BackSpace>', self.entry_bs)
        master.bind("<Key>", self.key_pressed)

    def create_label(self, text, row, col):
        """Create a label widget."""
        label = Label(self.frame, text=text, font=self.font)
        label.grid(column=col, row=row)
        return label

    def create_textfield(self, text, row, col):
        """Create a text field widget."""
        text_field = Text(self.frame, height=1, width=self.width, font=self.font)
        text_field.insert(END, text)
        text_field.grid(column=col, row=row)
        return text_field

    def create_entry(self, text, width, row, col):
        """Create an entry widget."""
        textbox = Entry(self.frame, width=width, font=self.font)
        textbox.grid(column=col, row=row)
        textbox.insert(END, text)
        return textbox

    def create_button(self, command, text, height, width, row, col):
        """Create a button widget."""
        button = Button(master=self.frame, command=command, height=height, width=width, text=text,
                        bg="green", font=self.font)
        button.grid(column=col, row=row)
        return button

    # Record Loading and Saving Functions
    def load_records(self):
        """Load records from CSV files."""
        self.record = self.load_csv('Touch-Typing-Trainer-[GH]/record.csv')
        self.record = [x for x in self.record if x]
        if len(self.record) < 5:
            self.reset(event=1)

    def save_csv(self, filename, data):
        """Save data to a CSV file."""
        with open(filename, "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(data)

    def clean_and_save_records(self):
        """Clean and save the records to CSV files."""
        self.record = [x for x in self.record if x and x[0] != " "]
        self.record.append([" ", 1, 0, 0, float(self.record[-1][4])])
        self.save_csv("Touch-Typing-Trainer-[GH]/record.csv", self.record)
        self.save_csv("Touch-Typing-Trainer-[GH]/monogram.csv", self.monogram.items())
        self.save_csv("Touch-Typing-Trainer-[GH]/bigram2.csv", self.bigram.items())
        self.save_csv("Touch-Typing-Trainer-[GH]/trigram2.csv", self.trigram.items())

    # Data Processing Functions

    def set_space(self, target=800):
        """Adjust the space character in the keylist to achieve the target score."""
        full_letters = self.text_letters.get("1.0", "end-1c")
        space_idx = full_letters.find(" ")

        while self.score < target and space_idx < len(full_letters):
            space_idx += 1
            full_letters = self.text_letters.get("1.0", "end-1c")
            subset_with_space = full_letters[:space_idx + 1]
            letter_subset = subset_with_space.replace(" ", "")
            encountered_letters = set(letter_subset)
            last_letter = letter_subset[-1] if letter_subset else ""
            
            vowels = {c for c in encountered_letters if c in "aeiou"}
            consonants = {c for c in encountered_letters if c.islower() and c not in "aeiou"}
            others = encountered_letters - vowels - consonants

            worst_vowels = sorted(vowels, key=lambda k: -float(self.monogram.get(k, 0)))[:]
            worst_consonants = sorted(consonants, key=lambda k: -float(self.monogram.get(k, 0)))[:]
            worst_others = sorted(others, key=lambda k: -float(self.monogram.get(k, 0)))[:]

            remaining_consonants = list(consonants - set(worst_consonants))
            helpers = random.sample(remaining_consonants, min(3, len(remaining_consonants)))

            selected_letters = set(worst_vowels) | set(worst_consonants) | set(worst_others) | set(helpers)
            if last_letter:
                selected_letters.add(last_letter)

            self.keylist = "".join(sorted(selected_letters))
            print(self.keylist)

            new_letters = letter_subset + " " + full_letters[space_idx + 1:]

            self.text_letters.config(state=tk.NORMAL)
            self.text_letters.delete("1.0", tk.END)
            self.text_letters.tag_remove("green", "1.0", tk.END)
            self.text_letters.tag_remove("purple", "1.0", tk.END)
            self.text_letters.tag_remove("orange", "1.0", tk.END)
            self.text_letters.tag_remove("red", "1.0", tk.END)

            # Store groupings for later use (e.g., in plot2)
            self.last_letter = last_letter
            self.group_vowel_helper = vowels.union(helpers)
            self.group_wc = set(worst_consonants)
            self.group_wo = set(worst_others)

            for i, c in enumerate(new_letters):
                self.text_letters.insert(tk.END, c)
                if c in self.keylist:
                    if c == self.last_letter:
                        tag = "purple"
                    elif c in self.group_wc:
                        tag = "orange"
                    elif c in self.group_wo:
                        tag = "red"
                    elif c in self.group_vowel_helper:
                        tag = "green"
                    else:
                        tag = "green"
                    self.text_letters.tag_add(tag, f"1.{i}", f"1.{i+1}")

            self.text_letters.config(state=tk.DISABLED)
            self.process_keylist()
            self.update_data_file()
            self.generate_words()
            self.update_labels()
            print(self.score)

    def process_keylist(self):
        """Read and process settings from the GUI."""
        self.keylistR = ''.join([char for char in self.keylist if char.islower()])
        self.keylistC = ''.join([char for char in self.keylist if char.isupper()])
        self.keylistC_conv = self.keylistC.lower()
        self.keylistN = ''.join([c for c in self.keylist if c in "0123456789.£$€%"])
        self.keylistP = ''.join([c for c in self.keylist if c in r""",.';:!?/-&^*=_+<>@#~\|"""])
        self.keylistB = ''.join([c for c in self.keylist if c in r""""([{"""])
        self.R_monograms = [[k, int(float(v))] for k, v in self.monogram.items() if k in self.keylistR]
        self.C_monograms = [[k, int(float(v))] for k, v in self.monogram.items() if k in self.keylistC]
        self.N_monograms = [[k, int(float(v))] for k, v in self.monogram.items() if k in self.keylistN]
        self.N_monograms_choice = [[k, int(float(v))] for k, v in self.monogram.items() if k in self.keylistN and k != "."]

        self.P_monograms = [[k, int(float(v))] for k, v in self.monogram.items() if k in self.keylistP]
        self.B_monograms = [[k, int(float(v))] for k, v in self.monogram.items() if k in self.keylistB]
        self.oldlen = len(self.ent_type.get())

    def update_data_file(self):
        """Update the data file with new frequency scores."""
        for row in self.data:
            row[2] = float(row[1]) ** 0.275893 / 13.30949
            row[3] = stat.mean([float(self.monogram[letter]) / 50 for letter in row[0] if letter in self.monogram])
            row[4] = self.calculate_bigram_score(row[0])
            row[5] = self.calculate_trigram_score(row[0])
            row[6] = row[2] ** self.w_freq * row[3] ** self.w_monogram * row[4] ** self.w_bigram * row[5] ** self.w_trigram
        self.save_csv("Touch-Typing-Trainer-[GH]/data2_10kcut.csv", self.data)

    def calculate_bigram_score(self, word):
        """Calculate the bigram score for a word."""
        if len(word) >= 2:
            bigram_scorelist = [float(self.bigram[word[i:i + 2]]) / 100 for i in range(len(word[1:])) if word[i:i + 2] in self.bigram]
            return stat.mean(bigram_scorelist) if bigram_scorelist else 1
        return 1

    def calculate_trigram_score(self, word):
        """Calculate the trigram score for a word."""
        if len(word) >= 3:
            trigram_scorelist = [float(self.trigram[word[i:i + 3]]) / 150 for i in range(len(word[2:])) if word[i:i + 3] in self.trigram]
            return stat.mean(trigram_scorelist) if trigram_scorelist else 1
        return 1

    # Word Generation and GUI Update Functions
    def generate_words(self):
        """Generate words and update the GUI."""
        self.printselected()
        self.letterpos = 0
        self.ent_type.delete(0, 'end')
        self.txt_words.delete("1.0", tk.END)
        self.penalty = -1
        self.penaltycount = 0
        self.partpenalty = -1
        self.partpenaltycount = 0
        self.error_list = []
        self.parterror_list = []
        self.txt_words.insert(END, self.printline)
        self.cleanmonogram = [[k, int(float(v))] for k, v in self.monogram.items() if any(k in word for word in self.wordlist)]
        self.cleanbigram = [[k, int(float(v))] for k, v in self.bigram.items() if any(k in word for word in self.wordlist)]
        self.cleantrigram = [[k, int(float(v))] for k, v in self.trigram.items() if any(k in word for word in self.wordlist)]

        self.oldscore = self.score
        self.scoreR1 = stat.mean([v for k, v in self.cleanmonogram])
        self.scoreR2 = stat.mean([v for k, v in self.cleanbigram])
        if self.cleantrigram:
            self.scoreR3 = stat.mean([v for k, v in self.cleantrigram])
            self.scoreR = (self.scoreR1 * self.scoreR2 / 2 * self.scoreR3 / 3) ** (1 / 3)
        else:
            self.scoreR = (self.scoreR1 * self.scoreR2 / 2) ** (1 / 2)

        self.scoreC = self.choose_matrix["C"]
        self.scoreN = self.choose_matrix["N"]
        self.scoreP = self.choose_matrix["P"]
        self.scoreB = self.choose_matrix["B"]
        # Count how many letters come from each category
        num_R = sum(1 for c in self.keylist if c in self.keylistR)
        num_C = sum(1 for c in self.keylist if c in self.keylistC)
        num_N = sum(1 for c in self.keylist if c in self.keylistN)
        num_P = sum(1 for c in self.keylist if c in self.keylistP)
        num_B = sum(1 for c in self.keylist if c in self.keylistB)

        # Total letters considered
        total = num_R + num_C + num_N + num_P + num_B

        # Avoid divide-by-zero by ensuring at least one category is present
        if total == 0:
            total = 1

        # Compute weight proportions
        weight_R = num_R / total
        weight_C = num_C / total
        weight_N = num_N / total
        weight_P = num_P / total
        weight_B = num_B / total

        # Compute final weighted score
        self.score = int(
            weight_R * self.scoreR +
            weight_C * self.scoreC +
            weight_N * self.scoreN +
            weight_P * self.scoreP +
            weight_B * self.scoreB
        )


    def update_labels(self):
        """Update labels in the GUI."""
        self.scorediff = int(self.score - self.oldscore)
        self.lbl_score2.config(text=f"{self.score} ({self.scorediff})")
        self.lbl_untouched2.config(
            text=f"Monograms ({len([v for k, v in self.cleanmonogram if v == 2000])}), "
                 f"Bigrams ({len([v for k, v in self.cleanbigram if v == 4000])}), "
                 f"Trigrams ({len([v for k, v in self.cleantrigram if v == 6000])})"
        )

    def update_action_record(self):
        """Update the action record and save it to a CSV file."""
        if self.oldlen > 0:
            self.action_record.append(
                [tm.time_ns(), self.oldlen, int(self.scoreR), int(self.scoreC), int(self.scoreN),
                 int(self.scoreP), int(self.scoreB), int(self.score), int(self.scorediff),
                 int(self.scoreR1), int(self.scoreR2 / 2), int(self.scoreR3 / 3)]
            )
        self.save_csv("Touch-Typing-Trainer-[GH]/action_record.csv", self.action_record)

    # Plotting Functions
    def plot(self):
        """Plot the performance metrics."""

        def rescale(y):
            return [(i + 20) / 40 if 0 <= (i + 20) / 40 <= 1 else (1 if (i + 20) / 40 > 1 else 0) for i in y]

        fig = Figure(figsize=(10, 4), dpi=100)
        self.subplot = fig.add_subplot(111)
        my_cmap = plt.get_cmap("RdYlGn_r")
        histlen = min(len(self.action_record), 10)
        val_score = [int(row[7]) for row in self.action_record]
        val_diff = [int(row[8]) for row in self.action_record]
        valR = [int(row[2]) for row in self.action_record]
        valC = [int(row[3]) for row in self.action_record]
        valN = [int(row[4]) for row in self.action_record]
        valP = [int(row[5]) for row in self.action_record]
        valB = [int(row[6]) for row in self.action_record]
        valR1 = [int(row[9]) for row in self.action_record]
        valR2 = [int(row[10]) for row in self.action_record]
        valR3 = [int(row[11]) for row in self.action_record]

        self.subplot.bar(range(-histlen, 0), val_score[-histlen:], tick_label=val_diff[-histlen:], color=my_cmap(rescale(val_diff[-histlen:])))
        self.subplot.plot(range(-histlen, 0), valR[-histlen:], color="k", linewidth=2, label="Regular")
        self.subplot.plot(range(-histlen, 0), valC[-histlen:], color="b", linewidth=2, label="Capital")
        self.subplot.plot(range(-histlen, 0), valN[-histlen:], color="m", linewidth=2)
        self.subplot.plot(range(-histlen, 0), valP[-histlen:], color="r", linewidth=2)
        self.subplot.plot(range(-histlen, 0), valB[-histlen:], color="c", linewidth=2)
        self.subplot.axhline(y=600, color='r', linestyle=':')
        self.subplot.axhline(y=800, color='orange', linestyle=':')
        self.subplot.legend()

        self.subplot.set_ylim([min(min(valR[-histlen:]), 500) - 10,
                               max([max(valR1[-histlen:]), max(valR2[-histlen:]), max(valR3[-histlen:]), max(valR[-histlen:]), max(valC[-histlen:]), max(valN[-histlen:]), max(valP[-histlen:]),
                                    max(valB[-histlen:]), max(val_score[-histlen:])]) + 10])
        self.img_plot = FigureCanvasTkAgg(fig, master=self.frame)
        self.img_plot.get_tk_widget().grid(row=self.gui_row, column=1)

    def plot2(self):
        """Plot the monogram frequency distribution."""
        fig2 = Figure(figsize=(10, 2), dpi=100)
        self.subplot2 = fig2.add_subplot(111)

        M = [int(float(v)) for k, v in self.monogram.items()]
        D = [M[0]]
        for i in range(1, len(M)):
            D.append(M[i])

        # Determine colours per letter based on groups defined in set_space
        colors = []
        for letter in self.monogram.keys():
            if hasattr(self, "last_letter") and letter == self.last_letter:
                colors.append("purple")
            elif hasattr(self, "group_wc") and letter in self.group_wc:
                colors.append("orange")
            elif hasattr(self, "group_wo") and letter in self.group_wo:
                colors.append("red")
            elif hasattr(self, "group_vowel_helper") and letter in self.group_vowel_helper:
                colors.append("green")
            else:
                colors.append("blue")

        self.subplot2.bar(range(len(D)), D, align='center', tick_label=list(self.monogram.keys()), color=colors)
        self.subplot2.axhline(y=600, color='r', linestyle='--')
        self.subplot2.axhline(y=800, color='orange', linestyle='--')
        self.subplot2.set_ylim([0, 2000])
        self.subplot2.set_xlim([-0.5, len(D) - 0.5])

        self.img_plot2 = FigureCanvasTkAgg(fig2, master=self.frame)
        self.img_plot2.get_tk_widget().grid(row=self.gui_row + 1, column=1)

    # Event Handling Functions
    def action(self, event=None):
        """Handle the main action triggered by pressing Enter."""
        self.clean_and_save_records()
        self.process_keylist()
        self.update_data_file()
        self.generate_words()
        self.update_labels()
        self.set_space(target=800)  # Run set_space after score calculation
        self.update_action_record()
        self.plot()
        self.plot2()
        self.frame.after(100, lambda: self.ent_type.focus_force())

    def key_pressed(self, event):
        """Handle key press events and update the GUI accordingly."""
        text_so_far = self.ent_type.get()
        self.current_pos = len(text_so_far) - 1
        if event.char:
            if self.current_pos == self.letterpos:  # full match to next letter
                if text_so_far == self.printline[:self.letterpos + 1]:
                    self.log_record(event)
                    if self.penalty == self.current_pos:
                        self.error_list.append(int(self.letterpos))
                    self.letterpos += 1
                    self.penalty = -1
                    self.partpenalty = -1
                    self.partpenaltycount = 0
                else:
                    self.penaltycount += 1
                    self.penalty = self.current_pos
            else:  # partial match
                if text_so_far == self.printline[:self.current_pos + 1]:
                    self.log_record(event)
                    if self.partpenalty == self.current_pos:
                        self.parterror_list.append(int(self.current_pos))
                        self.partpenalty = -1
                        self.partpenaltycount = 0
                else:
                    if self.partpenalty == -1:
                        self.partpenalty = self.current_pos
                        self.partpenaltycount = 1
                    elif self.partpenalty < self.current_pos:
                        pass
                    elif self.partpenalty > self.current_pos:
                        self.partpenalty = self.current_pos
                        self.partpenaltycount = 1
                    else:
                        self.partpenaltycount += 1
            self.bcksp = False
        self.highlight_typed_letters()
        if self.letterpos == len(self.printline):
            self.action()

    def highlight_typed_letters(self):
        """Highlight typed letters in the text field."""
        self.txt_words.delete("1.0", tk.END)
        for i, c in enumerate(self.printline):
            if i >= self.letterpos:
                self.txt_words.insert(END, c)
                continue
            if i in self.error_list:
                self.txt_words.insert(END, c, "error")
            elif i in self.parterror_list:
                self.txt_words.insert(END, c, "part")
            else:
                self.txt_words.insert(END, c, "correct")

    def entry_ctrl_bs(self, event):
        """Handle Ctrl+Backspace event."""
        ent = event.widget
        idx = ent.get().rfind(" ")
        ent.delete(0 if idx == -1 else idx + 1, END)
        self.bcksp = True

    def entry_bs(self, event):
        """Handle Backspace event."""
        self.bcksp = True

    def log_record(self, event):
        """Log the timings and other metrics to the records."""
        letter_time = (tm.time_ns() - float(self.record[-1][1])) / (10 ** 6) + (
                (self.penalty != -1) * self.penaltycount * 100) + (
                              (self.partpenalty != -1) * self.partpenaltycount * 100)
        if event.char != " " and (letter_time > 2000 or self.current_pos == 0 or self.bcksp):
            letter_time = float(self.monogram[event.char])
        letter_wpm = 0.66 * 12 * (10 ** 3) / letter_time
        ema_wpm = 0.01 * letter_wpm + 0.99 * float(self.record[-1][4])
        self.record.append(
            [event.char, tm.time_ns(), round(letter_time, 3), round(letter_wpm, 3), round(ema_wpm, 3)]
        )
        self.update_monogram_bigram_trigram(event, letter_time)
        self.lbl_wpm2.config(text=f"{int(ema_wpm)} WPM")

    def update_monogram_bigram_trigram(self, event, letter_time):
        """Update the monogram, bigram, and trigram values based on the current input."""
        self.monogram |= {k: 0.02 * letter_time + 0.98 * float(self.monogram[k]) for k in self.monogram if k == event.char}
        bigram_time = letter_time * 2
        self.bigram |= {k: 0.1 * bigram_time + 0.9 * float(self.bigram[k]) for k in self.bigram if k == str(self.record[-2][0] + event.char)}
        trigram_time = (letter_time + float(self.record[-2][2])) * 1.5
        self.trigram |= {k: 0.2 * trigram_time + 0.8 * float(self.trigram[k]) for k in self.trigram if k == str(self.record[-3][0] + self.record[-2][0] + event.char)}

    # Reset Function
    def reset(self, event):
        """Reset the records and data to initial values."""
        self.total_letters = 0
        self.start_time = tm.time_ns()
        self.monogram = {x: 2000 for x in self.monogram}
        self.bigram = {x: 4000 for x in self.bigram}
        self.trigram = {x: 6000 for x in self.trigram}
        self.record = [["e", 1, 0, 0, 0], ["e", 1, 0, 0, 50]]
        self.action_record = [[tm.time_ns(), 60, 2000, 2000, 2000, 2000, 2000, 2000, 0, 2000, 2000, 2000]]
        for row in self.data:
            row[3] = row[4] = row[5] = 1
        self.txt_words.delete("1.0", tk.END)
        self.txt_words.insert(END, "RESET RECORDS")
        self.save_csv("Touch-Typing-Trainer-[GH]/action_record.csv", self.action_record)
        self.save_csv("Touch-Typing-Trainer-[GH]/record.csv", self.record)
        self.save_csv("Touch-Typing-Trainer-[GH]/monogram.csv", self.monogram.items())
        self.save_csv("Touch-Typing-Trainer-[GH]/bigram2.csv", self.bigram.items())
        self.save_csv("Touch-Typing-Trainer-[GH]/trigram2.csv", self.trigram.items())


# Main Function: Initializes and runs the tkinter main loop.
def main():
    root = Tk()
    root.title("Smart Typer v5.1")
    window = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
