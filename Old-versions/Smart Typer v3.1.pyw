import csv
import random
import statistics as stat
import time as tm
import tkinter as tk
from tkinter import *

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure


class Wordset():
    def __init__(self):
        with open('data2_10kcut.csv') as csvfile:
            self.data = list(csv.reader(csvfile, delimiter=","))
            self.data[0][0] = "the"
        with open('monogram.csv') as csvfile:
            self.monogram = {rows[0]: rows[1]
                             for rows in (csv.reader(csvfile, delimiter=","))}
        with open('bigram2.csv') as csvfile:
            self.bigram = {rows[0]: rows[1]
                           for rows in (csv.reader(csvfile, delimiter=","))}
        with open('trigram2.csv') as csvfile:
            self.trigram = {rows[0]: rows[1]
                            for rows in (csv.reader(csvfile, delimiter=","))}
        with open('action_record.csv') as csvfile:
            self.action_record = list(csv.reader(csvfile, delimiter=","))

    keylist = "a"
    keylistR = "a"
    keylistC = "A"
    keylistC_conv = "a"
    keylistN = "0"
    keylistP = ","
    keylistB = "("
    minsize = 1
    printline = ""
    R_monograms = []
    C_monograms = []
    N_monograms = []
    N_monograms_choice = []
    P_monograms = []
    B_monograms = []

    def isallowed(self, word):
        if len(word) < self.minsize:
            return False
        else:
            for letter in word:
                if letter not in self.keylistR:
                    return False
            return True

    def search_words(self):
        self.activelist = []
        i = 0
        for line in self.data:
            word = line[0]
            if self.isallowed(word):
                self.activelist.append(line)

    def choose_regular(self):
        select_word = np.random.choice(
            a=self.wordlist, size=1, p=self.freqlist)[0]
        return select_word

    def isallowedC(self, word):
        if len(word) < self.minsize:
            return False
        elif word[0] not in self.keylistC_conv:
            return False
        else:
            for letter in word[1:]:
                if letter not in self.keylistR:
                    return False
            return True

    def search_wordsC(self):
        self.activelistC = []
        i = 0
        for line in self.data:
            word = line[0]
            if self.isallowedC(word):
                self.activelistC.append(line)

    def choose_capital(self):
        select_word = np.random.choice(
            a=self.wordlistC, size=1, p=self.freqlistC)[0]
        return select_word.capitalize()

    def choose_number(self):
        wordlen = random.randint(3, 7)
        select_word = ""
        for i in range(wordlen):
            char = np.random.choice(
                a=self.wordlistN, size=1, p=self.freqlistN)[0]
            if i == 0:
                while char in ".%":
                    char = np.random.choice(
                        a=self.wordlistN, size=1, p=self.freqlistN)[0]
            elif i == 1:
                while char in ".£$€%":
                    char = np.random.choice(
                        a=self.wordlistN, size=1, p=self.freqlistN)[0]
            elif i == wordlen - 1:
                while char in ".£$€":
                    char = np.random.choice(
                        a=self.wordlistN, size=1, p=self.freqlistN)[0]
            else:
                while char in "£$€%":
                    char = np.random.choice(
                        a=self.wordlistN, size=1, p=self.freqlistN)[0]
            select_word += char
        return select_word

    def modify_punc(self, word):
        char = np.random.choice(a=self.wordlistP, size=1, p=self.freqlistP)[0]
        return word + char

    def modify_bracket(self, word):
        char = np.random.choice(a=self.wordlistB, size=1, p=self.freqlistB)[0]
        if char == '"':
            char2 = '"'
        elif char == "(":
            char2 = ")"
        elif char == "[":
            char2 = "]"
        else:
            char2 = "}"
        return char + word + char2

    def choosewords(self):
        self.search_words()
        self.search_wordsC()
        self.selected = []

        # Set up frequency selection for each case
        self.wordlist = [row[0] for row in self.activelist]
        self.freqlist = [int(row[6]) for row in self.activelist]
        freqsum = sum(self.freqlist)
        self.freqlist[:] = [n / freqsum for n in self.freqlist]

        self.wordlistC = [row[0] for row in self.activelistC]
        self.freqlistC = [int(row[6]) for row in self.activelistC]
        freqsumC = sum(self.freqlistC)
        self.freqlistC[:] = [n / freqsumC for n in self.freqlistC]

        self.wordlistN = [k for k, v in self.N_monograms]
        self.freqlistN = [int(float(v)) for k, v in self.N_monograms]
        freqsumN = sum(self.freqlistN)
        self.freqlistN[:] = [n / freqsumN for n in self.freqlistN]

        self.wordlistP = [k for k, v in self.P_monograms]
        self.freqlistP = [int(float(v)) for k, v in self.P_monograms]
        freqsumP = sum(self.freqlistP)
        self.freqlistP[:] = [n / freqsumP for n in self.freqlistP]

        self.wordlistB = [k for k, v in self.B_monograms]
        self.freqlistB = [int(float(v)) for k, v in self.B_monograms]
        freqsumB = sum(self.freqlistB)
        self.freqlistB[:] = [n / freqsumB for n in self.freqlistB]

        # building final word list
        self.choose_matrix = {}

        # calculate mean scores for each type
        if len(self.R_monograms) == 0:
            self.choose_matrix['R'] = 0
        else:
            self.choose_matrix['R'] = stat.mean(
                [v for k, v in self.R_monograms])
        if len(self.C_monograms) == 0:
            self.choose_matrix['C'] = 0
        else:
            self.choose_matrix['C'] = stat.mean(
                [v for k, v in self.C_monograms])
        if len(self.N_monograms_choice) == 0:
            self.choose_matrix['N'] = 0
        else:
            self.choose_matrix['N'] = stat.mean(
                [v for k, v in self.N_monograms_choice])
        if len(self.P_monograms) == 0:
            self.choose_matrix['P'] = 0
        else:
            self.choose_matrix['P'] = stat.mean(
                [v for k, v in self.P_monograms])
        if len(self.B_monograms) == 0:
            self.choose_matrix['B'] = 0
        else:
            self.choose_matrix['B'] = stat.mean(
                [v for k, v in self.B_monograms])

        self.wordlistM = [
            k for k, v in self.choose_matrix.items() if k in "RCN"]
        self.freqlistM = [int(float(v))
                          for k, v in self.choose_matrix.items() if k in "RCN"]
        freqsumM = sum(self.freqlistM)
        self.freqlistM[:] = [n / freqsumM for n in self.freqlistM]

        self.wordlistM2 = [k for k, v in self.choose_matrix.items()]
        self.freqlistM2 = [int(float(v))
                           for k, v in self.choose_matrix.items()]
        freqsumM2 = sum(self.freqlistM2)
        self.freqlistM2[:] = [n / freqsumM2 for n in self.freqlistM2]

        selected_length = 0
        while selected_length < 60:
            classtype = np.random.choice(
                a=self.wordlistM, size=1, p=self.freqlistM)[0]
            if classtype == "R":
                select_word = self.choose_regular()
            elif classtype == "C":
                select_word = self.choose_capital()
            else:
                select_word = self.choose_number()
            classtype2 = np.random.choice(
                a=self.wordlistM2, size=1, p=self.freqlistM2)[0]
            if classtype2 == "P":
                select_word = self.modify_punc(select_word)
            elif classtype2 == "B":
                select_word = self.modify_bracket(select_word)
            else:
                pass

            if selected_length + len(select_word) <= 60:
                selected_length += len(select_word)
                self.selected.append(select_word)
            else:
                break

    def printselected(self):
        self.choosewords()
        self.printline = ""
        for word in self.selected:
            self.printline += str(word) + " "
        self.printline += " "


class MainWindow(Wordset):
    def __init__(self, master):
        Wordset.__init__(self)
        self.frame = Frame(master)
        # make GUI objects
        gui_row = 0
        self.lbl_letters = self.create_label(
            self.frame, "Letters:", gui_row, 0)
        self.ent_letters = self.create_entry(self.frame, "aorisetndhqwyfuplgjzxcmvkbAORISETNDHQWYFUPLGJZXCMVKB ", 70,
                                             gui_row, 1)
        gui_row += 1
        self.lbl_symbols = self.create_label(
            self.frame, "Symbols:", gui_row, 0)
        self.ent_symbols = self.create_entry(self.frame, """,.'"(;:!?/-0123456789%£$€&^*=_+<>@[{#~\| """, 70,
                                             gui_row, 1)
        gui_row += 1
        self.lbl_untouched = self.create_label(
            self.frame, "Untouched", gui_row, 0)
        self.lbl_untouched2 = self.create_label(self.frame, "", gui_row, 1)
        gui_row += 1
        self.lbl_score = self.create_label(
            self.frame, "Score (T<400)", gui_row, 0)
        self.lbl_score2 = self.create_label(self.frame, "", gui_row, 1)
        gui_row += 1
        self.lbl_words = self.create_label(
            self.frame, "Generated words:", gui_row, 0)
        self.txt_words = self.create_textfield(self.frame, "", gui_row, 1)
        self.txt_words.tag_config("correct", background="green")
        self.txt_words.tag_config("error", background="red")
        gui_row += 1
        self.lbl_type = self.create_label(self.frame, "Type here:", gui_row, 0)
        self.ent_type = self.create_entry(self.frame, "", 70, gui_row, 1)
        self.ent_type.config(background="yellow")
        self.lbl_wpm2 = self.create_label(self.frame, "?? WPM", gui_row, 2)
        gui_row += 1
        self.but_fig = self.create_button(self.frame, self.switch_fig, "Show/Hide" + "\n" + "Keyboard", 2, 15, gui_row,
                                          0)
        self.gui_row = gui_row
        gui_row += 1
        self.lbl_placeholder = self.create_label(
            self.frame, "Copyright Marij Qureshi 2021", gui_row + 1, 1)

        # set bindings
        master.bind('<Return>', self.action)
        master.bind('<Control-r>', self.reset)
        master.bind("<Key>", self.key_pressed)
        # load record files
        with open('record.csv') as csvfile:
            self.record = list(csv.reader(csvfile, delimiter=","))
        self.record = [x for x in self.record if x]
        if len(self.record) < 5:
            self.reset(event=1)
        self.action(event=1)
        self.frame.pack()

    font = ("Calibri", 28)
    total_letters = 0
    start_time = tm.time()
    nextletter = ""
    letterpos = 0
    width = 70
    img_toggle = 0
    w_freq = 1
    w_monogram = 1
    w_bigram = 1
    w_trigram = 1
    score = 0
    penalty = False
    error_list = []

    def create_label(self, frame, text, row, col):
        label = Label(frame, text=text, font=self.font)
        label.grid(column=col, row=row)
        return label

    def create_textfield(self, frame, text, row, col):
        label = Text(frame, height=1, width=self.width, font=self.font)
        label.insert(END, text)
        label.grid(column=col, row=row)
        return label

    def create_entry(self, frame, text, width, row, col):
        textbox = Entry(frame, width=width, font=self.font)
        textbox.grid(column=col, row=row)
        textbox.insert(END, text)
        return textbox

    def create_button(self, frame, command, text, height, width, row, col):
        button = Button(master=frame, command=command, height=height, width=width, text=text, bg="green",
                        font=self.font)
        button.grid(column=col, row=row)
        return button

    def disp_image(self):
        image = tk.PhotoImage(file="image.png")
        self.lbl_image = tk.Label(self.frame, image=image)
        self.lbl_image.image = image
        self.lbl_image.grid(row=self.gui_row, column=1)
        self.frame.pack()

    def switch_fig(self):
        if self.img_toggle == 0:
            self.img_plot.get_tk_widget().delete("all")
            self.disp_image()
            self.img_toggle = 1
        else:
            self.lbl_image.grid_forget()
            self.img_toggle = 0
            self.plot()

    def plot(self):
        def rescale(y):
            result = []
            for i in y:
                k = (i + 20) / 40
                if k > 1:
                    result.append(1)
                elif k < 0:
                    result.append(0)
                else:
                    result.append(k)
            return result

        if self.img_toggle == 0:
            fig = Figure(figsize=(10, 4), dpi=100)
            self.subplot = fig.add_subplot(111)
            my_cmap = plt.get_cmap("RdYlGn_r")
            histlen = min(len(self.action_record), 10)
            val_score = [int(row[7]) for row in self.action_record]
            valR = [int(row[2]) for row in self.action_record]
            valC = [int(row[3]) for row in self.action_record]
            valN = [int(row[4]) for row in self.action_record]
            valP = [int(row[5]) for row in self.action_record]
            valB = [int(row[6]) for row in self.action_record]
            val_diff = [int(row[8]) for row in self.action_record]
            valR1 = [int(row[9]) for row in self.action_record]
            valR2 = [int(row[10]) for row in self.action_record]
            valR3 = [int(row[11]) for row in self.action_record]

            self.subplot.bar(range(-histlen, 0), val_score[-histlen:], tick_label=val_diff[-histlen:],
                             color=my_cmap(rescale(val_diff[-histlen:])))
            self.subplot.plot(
                range(-histlen, 0), valR[-histlen:], color="k", linewidth=2, label="Regular")
            self.subplot.plot(range(-histlen, 0),
                              valC[-histlen:], color="b", linewidth=2, label="Capital")
            self.subplot.plot(range(-histlen, 0),
                              valN[-histlen:], color="m", linewidth=2)
            self.subplot.plot(range(-histlen, 0),
                              valP[-histlen:], color="r", linewidth=2)
            self.subplot.plot(range(-histlen, 0),
                              valB[-histlen:], color="c", linewidth=2)
            self.subplot.plot(
                range(-histlen, 0), valR1[-histlen:], color="b", linewidth=2, linestyle='--', label="Single")
            self.subplot.plot(
                range(-histlen, 0), valR2[-histlen:], color="m", linewidth=2, linestyle='--', label="Double")
            self.subplot.plot(
                range(-histlen, 0), valR3[-histlen:], color="c", linewidth=2, linestyle='--', label="Triple")
            self.subplot.axhline(y=400, color='r', linestyle='--')
            self.subplot.legend()

            self.subplot.set_ylim(
                [min(min(valR[-histlen:]), min(valR1[-histlen:]), min(valR2[-histlen:]), min(valR3[-histlen:]),
                     400) - 10,
                 max([max(valR1[-histlen:]), max(valR2[-histlen:]), max(valR3[-histlen:]), max(valR[-histlen:]),
                      max(valC[-histlen:]), max(valN[-histlen:]
                                                ), max(valP[-histlen:]),
                      max(valB[-histlen:]), max(val_score[-histlen:])]) + 10])
            self.img_plot = FigureCanvasTkAgg(fig, master=self.frame)
            self.img_plot.get_tk_widget().grid(row=self.gui_row, column=1)

    def plot2(self):
        def rescale(y):
            result = []
            for i in y:
                k = (i + 20) / 40
                if k > 1:
                    result.append(1)
                elif k < 0:
                    result.append(0)
                else:
                    result.append(k)
            return result

        fig2 = Figure(figsize=(10, 2), dpi=100)
        self.subplot2 = fig2.add_subplot(111)
        M = [int(float(v)) for k, v in self.monogram.items()]
        D = [M[0]]
        for i in range(1, len(M)):
            D.append((i / (i + 1)) * D[i - 1] + (1 / (i + 1)) * M[i])
        self.subplot2.bar(range(len(D)), D, align='center',
                          tick_label=list(self.monogram.keys()))
        self.subplot2.axhline(
            y=400 + (self.scoreR1 - self.scoreR), color='r', linestyle='--')
        self.subplot2.set_ylim([0, 2000])
        self.subplot2.set_xlim([-0.5, len(D) - 0.5])
        self.img_plot2 = FigureCanvasTkAgg(fig2, master=self.frame)
        self.img_plot2.get_tk_widget().grid(row=self.gui_row + 1, column=1)

    def action(self, event):
        # clean/save record
        self.record = [x for x in self.record if x]
        self.record = [x for x in self.record if x[0] != " "]
        self.record.append([" ", 1, 0, 0, float(self.record[-1][4])])
        with open("record.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.record)
        with open("monogram.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.monogram.items())
        with open("bigram2.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.bigram.items())
        with open("trigram2.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.trigram.items())

        # read settings
        full_letters = self.ent_letters.get()
        full_symbols = self.ent_symbols.get()
        if full_letters.find(" ") == len(full_letters) - 1:
            self.keylist = full_letters[:-1] + \
                full_symbols[:full_symbols.find(" ")]
        else:
            self.keylist = full_letters[:full_letters.find(" ")]
        self.keylistR = self.keylist[:min(len(self.keylist), 26)]
        self.keylistC = self.keylist[min(
            len(self.keylist), 26):min(len(self.keylist), 52)]
        self.keylistC_conv = self.keylistC.lower()
        self.keylistN = ''.join(
            [c for c in self.keylist if c in "0123456789.£$€%"])
        self.keylistP = ''.join(
            [c for c in self.keylist if c in """,.';:!?/-&^*=_+<>@#~\|"""])
        self.keylistB = ''.join([c for c in self.keylist if c in """"([{"""])
        self.R_monograms = [
            [k, int(float(v))] for k, v in self.monogram.items() if k in self.keylistR]
        self.C_monograms = [
            [k, int(float(v))] for k, v in self.monogram.items() if k in self.keylistC]
        self.N_monograms = [
            [k, int(float(v))] for k, v in self.monogram.items() if k in self.keylistN]
        self.N_monograms_choice = [[k, int(float(v))] for k, v in self.monogram.items() if
                                   k in self.keylistN and k != "."]
        self.P_monograms = [
            [k, int(float(v))] for k, v in self.monogram.items() if k in self.keylistP]
        self.B_monograms = [
            [k, int(float(v))] for k, v in self.monogram.items() if k in self.keylistB]
        self.oldlen = len(self.ent_type.get())

        # update data file
        for row in self.data:
            row[2] = float(row[1]) ** 0.275893 / 13.30949
            monogram_score = float(self.monogram[row[0][0]]) / 50
            for letter in row[0][1:]:
                if letter in self.monogram:
                    monogram_score = stat.mean(
                        [monogram_score, float(self.monogram[letter]) / 50])
            row[3] = monogram_score

            if len(row[0]) >= 2:
                bigram_scorelist = []
                for i in range(len(row[0][1:])):
                    if row[0][i:i + 2] in self.bigram:
                        bigram_scorelist.append(
                            float(self.bigram[row[0][i:i + 2]]) / 100)
                bigram_score = stat.mean(bigram_scorelist)
            else:
                bigram_score = 1

            if len(row[0]) >= 3:
                trigram_scorelist = []
                for i in range(len(row[0][2:])):
                    if row[0][i:i + 3] in self.trigram:
                        trigram_scorelist.append(
                            float(self.trigram[row[0][i:i + 3]]) / 150)
                trigram_score = stat.mean(trigram_scorelist)
            else:
                trigram_score = 1
            row[4] = bigram_score
            row[5] = trigram_score
            row[6] = row[2] ** self.w_freq * \
                row[3] ** self.w_monogram * \
                row[4] ** self.w_bigram * \
                row[5] ** self.w_trigram
        with open("data2_10kcut.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.data)
        # generate words
        self.printselected()
        self.letterpos = 0
        self.nextletter = self.printline[self.letterpos]
        # update labels
        self.ent_type.delete(0, 'end')
        self.txt_words.delete("1.0", tk.END)
        self.penalty = False
        self.error_list = []
        self.txt_words.insert(END, self.printline)
        self.cleanmonogram = [[k, int(float(v))] for k, v in self.monogram.items() if
                              any(k in word for word in self.wordlist)]
        self.cleanbigram = [[k, int(float(v))] for k, v in self.bigram.items() if
                            any(k in word for word in self.wordlist)]
        self.cleantrigram = [[k, int(float(v))] for k, v in self.trigram.items() if
                             any(k in word for word in self.wordlist)]
        self.oldscore = self.score
        self.scoreR1 = stat.mean([v for k, v in self.cleanmonogram])
        self.scoreR2 = stat.mean([v for k, v in self.cleanbigram])
        self.scoreR3 = stat.mean([v for k, v in self.cleantrigram])
        self.scoreR = (self.scoreR1 * self.scoreR2 /
                       2 * self.scoreR3 / 3) ** (1 / 3)
        self.scoreC = self.choose_matrix["C"]
        self.scoreN = self.choose_matrix["N"]
        self.scoreP = self.choose_matrix["P"]
        self.scoreB = self.choose_matrix["B"]
        self.score = self.scoreR
        rootcount = 1
        if self.choose_matrix["C"] > 0:
            self.score *= self.scoreC
            rootcount += 1
        if self.choose_matrix["N"] > 0:
            self.score *= self.scoreN
            rootcount += 1
        if self.choose_matrix["P"] > 0:
            self.score *= self.scoreP
            rootcount += 1
        if self.choose_matrix["B"] > 0:
            self.score *= self.scoreB
            rootcount += 1
        self.score = int(self.score ** (1 / rootcount))
        self.scorediff = int(self.score - self.oldscore)
        self.lbl_score2.config(text=str(self.score) +
                               " (" + str(self.scorediff) + ")")
        self.lbl_untouched2.config(
            text="Monograms (" +
            str(len([v for k, v in self.cleanmonogram if v == 2000])) + "), "
            + "Bigrams (" + str(len([v for k, v in self.cleanbigram if v == 4000])) + "), "
            + "Trigrams (" + str(len([v for k, v in self.cleantrigram if v == 6000])) + ")")
        # update action_record
        if self.oldlen > 0:
            self.action_record.append(
                [tm.time_ns(), self.oldlen, int(self.scoreR), int(self.scoreC), int(self.scoreN), int(self.scoreP),
                 int(self.scoreB), int(self.score), int(self.scorediff), int(
                     self.scoreR1), int(self.scoreR2 / 2),
                 int(self.scoreR3 / 3)])
        self.plot()
        self.plot2()
        with open("action_record.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.action_record)
        self.frame.after(100, lambda: self.ent_type.focus_force())

    def reset(self, event):
        self.total_letters = 0
        self.start_time = tm.time_ns()
        self.monogram = {x: 2000 for x in self.monogram}
        self.bigram = {x: 4000 for x in self.bigram}
        self.trigram = {x: 6000 for x in self.trigram}
        self.record = [["e", 1, 0, 0, 0], ["e", 1, 0, 0, 50]]
        self.action_record = [
            [tm.time_ns(), 60, 2000, 2000, 2000, 2000, 2000, 2000, 0, 2000, 2000, 2000]]
        for row in self.data:
            row[3] = row[4] = row[5] = 1
        self.txt_words.delete("1.0", tk.END)
        self.txt_words.insert(END, "RESET RECORDS")
        # Save files
        with open("action_record.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.action_record)
        with open("record.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.record)
        with open("monogram.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.monogram.items())
        with open("bigram2.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.bigram.items())
        with open("trigram2.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.trigram.items())

    def key_pressed(self, event):
        text_so_far = self.ent_type.get()
        if event.char == self.nextletter and text_so_far == self.printline[:self.letterpos + 1]:
            if self.penalty:
                self.error_list.append(int(self.letterpos))
            self.letterpos += 1
            letter_time = (
                tm.time_ns() - float(self.record[-1][1])) / (10 ** 6) + (self.penalty * 50)
            if (letter_time > 2000 or self.letterpos == 1) and event.char != " ":
                letter_time = float(self.monogram[event.char])
            letter_wpm = 0.66 * 12 * (10 ** 3) / letter_time
            ema_wpm = 0.01 * letter_wpm + 0.99 * float(self.record[-1][4])
            self.record.append(
                [event.char, tm.time_ns(), round(letter_time, 3), round(letter_wpm, 3), round(ema_wpm, 3)])
            self.monogram |= {k: 0.02 * letter_time + 0.98 * float(self.monogram[k])
                              for k in self.monogram if k == event.char}
            bigram_time = letter_time * 2
            self.bigram |= {k: 0.1 * bigram_time + 0.9 * float(self.bigram[k])
                            for k in self.bigram if k == str(self.record[-2][0] + event.char)}
            trigram_time = (letter_time + float(self.record[-2][2])) * 1.5
            self.trigram |= {k: 0.2 * trigram_time + 0.8 * float(self.trigram[k])
                             for k in self.trigram if k == str(self.record[-3][0] + self.record[-2][0] + event.char)}
            self.lbl_wpm2.config(text=str(int(ema_wpm)) + " WPM")
            self.penalty = False
        elif self.letterpos > 0 and text_so_far[:-1] == self.printline[:self.letterpos] and text_so_far[-1] != self.printline[self.letterpos]:
            self.penalty = True
        self.nextletter = self.printline[self.letterpos]
        # highlight typed letters
        self.txt_words.delete("1.0", tk.END)
        lasterror = 0
        for error in self.error_list:
            self.txt_words.insert(
                END, self.printline[lasterror:error], "correct")
            self.txt_words.insert(
                END, self.printline[error:error+1], "error")
            lasterror = error + 1
        self.txt_words.insert(
            END, self.printline[lasterror:self.letterpos], "correct")
        self.txt_words.insert(
            END, self.printline[self.letterpos:])
        # end of line auto action
        if self.letterpos == len(self.printline) - 1:
            self.action(event=1)


def main():
    root = Tk()
    root.title("Smart Typer v3.1")
    window = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
