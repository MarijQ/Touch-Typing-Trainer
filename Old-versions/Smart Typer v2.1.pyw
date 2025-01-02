"""
Strategy:
- 3 levels of experience:
    wordsmith (letters only + shift/backspace/space/enter)
    author (+ ",.!?();:)
    programmer (+ numbers + £$%^&*-=_+<>/@{}[]#~\|)

Next steps:
- Proper graphs

"""

import csv
import statistics as stat
import time as tm
import tkinter as tk
from operator import itemgetter
from tkinter import *

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure


class Wordset():
    def __init__(self):
        with open('data.csv') as csvfile:
            self.data = list(csv.reader(csvfile, delimiter=","))
            self.data[0][0] = "the"
        with open('monogram.csv') as csvfile:
            self.monogram = {rows[0]: rows[1] for rows in (csv.reader(csvfile, delimiter=","))}
        with open('bigram.csv') as csvfile:
            self.bigram = {rows[0]: rows[1] for rows in (csv.reader(csvfile, delimiter=","))}
        with open('trigram.csv') as csvfile:
            self.trigram = {rows[0]: rows[1] for rows in (csv.reader(csvfile, delimiter=","))}
        with open('action_record.csv') as csvfile:
            self.action_record = list(csv.reader(csvfile, delimiter=","))

    keylist = "abcdefghijk"
    minsize = 3
    numwords = 10
    printline = ""

    def isallowed(self, word):
        if len(word) < self.minsize:
            return False
        else:
            for letter in word:
                if letter not in self.keylist:
                    return False
            return True

    def search_words(self):
        self.activelist = []
        i = 0
        for line in self.data:
            word = line[0]
            if self.isallowed(word):
                self.activelist.append(line)

    def choosewords(self):
        self.selected = []
        self.wordlist = [row[0] for row in self.activelist]
        freqlist = [int(row[6]) for row in self.activelist]
        freqsum = sum(freqlist)
        freqlist[:] = [n / freqsum for n in freqlist]
        self.selected = np.random.choice(a=self.wordlist, size=self.numwords, p=freqlist)

    def printselected(self):
        self.printline = ""
        for word in self.selected:
            self.printline += str(word) + " "
        self.printline += " "
        # print(sum([len(word) for word in selected]))


class MainWindow(Wordset):
    def __init__(self, master):
        Wordset.__init__(self)
        self.frame = Frame(master)
        # make GUI objects
        self.lbl_letters = self.create_label(self.frame, "Allowed letters:", 0, 0)
        self.ent_letters = self.create_entry(self.frame, "aorisetndhqwyfuplgjzxcmvkb", 60, 0, 1)
        self.lbl_size = self.create_label(self.frame, "Minimum word size:", 1, 0)
        self.txt_size = self.create_entry(self.frame, "1", 60, 1, 1)
        self.lbl_nwords = self.create_label(self.frame, "Number of words:", 2, 0)
        self.txt_nwords = self.create_entry(self.frame, "10", 60, 2, 1)
        self.lbl_words = self.create_label(self.frame, "Generated words:", 3, 0)
        self.txt_words = self.create_textfield(self.frame, "", 3, 1)
        self.txt_words.tag_config("done", background="green")
        self.lbl_type = self.create_label(self.frame, "Type here:", 4, 0)
        self.ent_type = self.create_entry(self.frame, "", 60, 4, 1)
        self.ent_type.config(background="yellow")
        self.lbl_wpm = self.create_label(self.frame, "Current WPM:", 5, 0)
        self.lbl_wpm2 = self.create_label(self.frame, "", 5, 1)
        self.ent_freq = self.create_entry(self.frame, "1", 5, 5, 2)
        self.lbl_score = self.create_label(self.frame, "Score (T<400)", 6, 0)
        self.lbl_score2 = self.create_label(self.frame, "", 6, 1)
        self.lbl_monogram = self.create_label(self.frame, "Worst Monograms", 7, 0)
        self.lbl_monogram2 = self.create_label(self.frame, "", 7, 1)
        self.ent_monogram = self.create_entry(self.frame, "1", 5, 7, 2)
        self.lbl_bigram = self.create_label(self.frame, "Worst Bigrams", 8, 0)
        self.lbl_bigram2 = self.create_label(self.frame, "", 8, 1)
        self.ent_bigram = self.create_entry(self.frame, "1", 5, 8, 2)
        self.lbl_trigram = self.create_label(self.frame, "Worst Trigrams", 9, 0)
        self.lbl_trigram2 = self.create_label(self.frame, "", 9, 1)
        self.ent_trigram = self.create_entry(self.frame, "1", 5, 9, 2)
        self.but_fig = self.create_button(self.frame, self.switch_fig, "Show/Hide" + "\n" + "Keyboard", 2, 15, 10, 0)
        self.but_update = self.create_button(self.frame, self.plot, "Update", 2, 7, 10, 2)
        self.disp_image()
        # set bindings
        master.bind('<Return>', self.action)
        master.bind('<Control-r>', self.reset)
        master.bind("<Key>", self.key_pressed)
        # initialise variables
        self.w_freq = float(self.ent_freq.get())
        self.w_monogram = float(self.ent_monogram.get())
        self.w_bigram = float(self.ent_bigram.get())
        self.w_trigram = float(self.ent_trigram.get())
        self.minsize = int(self.txt_size.get())
        self.numwords = int(self.txt_nwords.get())
        self.keylist = self.ent_letters.get()
        self.score = 0
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
    width = 60
    img_toggle = 0

    def create_label(self, frame, text, row, col):
        label = Label(frame, text=text, font=self.font)
        label.grid(column=col, row=row)
        return label

    def create_textfield(self, frame, text, row, col):
        label = Text(frame, height=2, width=self.width, font=self.font)
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
        self.lbl_image.grid(row=10, column=1)
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

            histlen = 10
            val0 = [int(row[5]) for row in self.action_record]
            val1 = [int(row[2]) for row in self.action_record]
            val2 = [int(row[3]) / 2 for row in self.action_record]
            val3 = [int(row[4]) / 3 for row in self.action_record]
            val4 = [int(row[6]) for row in self.action_record]

            self.subplot.bar(range(-histlen, 0), val0[-histlen:], tick_label=val4[-histlen:],
                             color=my_cmap(rescale(val4[-histlen:])))
            self.subplot.plot(range(-histlen, 0), val1[-histlen:], color="k", linewidth=2)
            self.subplot.plot(range(-histlen, 0), val2[-histlen:], color="b", linewidth=2)
            self.subplot.plot(range(-histlen, 0), val3[-histlen:], color="m", linewidth=2)
            self.subplot.axhline(y=400, color='r', linestyle='--')

            self.subplot.set_ylim(
                [min(min(val1[-histlen:]), 400) - 10,
                 max([max(val0[-histlen:]), max(val1[-histlen:]), max(val2[-histlen:]),
                      max(val3[-histlen:]), max(val4[-histlen:])]) + 10])
            self.img_plot = FigureCanvasTkAgg(fig, master=self.frame)
            self.img_plot.get_tk_widget().grid(row=10, column=1)

    def plot2(self):
        pass

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
        with open("bigram.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.bigram.items())
        with open("trigram.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.trigram.items())
        # read settings
        self.w_freq = float(self.ent_freq.get())
        self.w_monogram = float(self.ent_monogram.get())
        self.w_bigram = float(self.ent_bigram.get())
        self.w_trigram = float(self.ent_trigram.get())
        self.minsize = int(self.txt_size.get())
        self.numwords = int(self.txt_nwords.get())
        self.keylist = self.ent_letters.get()
        self.oldlen = len(self.ent_type.get())
        # update data file
        for row in self.data:
            row[2] = float(row[1]) ** 0.275893 / 13.30949
            monogram_score = float(self.monogram[row[0][0]]) / 50
            for letter in row[0][1:]:
                if letter in self.monogram:
                    monogram_score = stat.mean([monogram_score, float(self.monogram[letter]) / 50])
            row[3] = monogram_score

            if len(row[0]) >= 2:
                bigram_scorelist = []
                for i in range(len(row[0][1:])):
                    if row[0][i:i + 2] in self.bigram:
                        bigram_scorelist.append(float(self.bigram[row[0][i:i + 2]]) / 100)
                bigram_score = stat.mean(bigram_scorelist)
            else:
                bigram_score = 1

            if len(row[0]) >= 3:
                trigram_scorelist = []
                for i in range(len(row[0][2:])):
                    if row[0][i:i + 3] in self.trigram:
                        trigram_scorelist.append(float(self.trigram[row[0][i:i + 3]]) / 150)
                trigram_score = stat.mean(trigram_scorelist)
            else:
                trigram_score = 1
            row[4] = bigram_score
            row[5] = trigram_score
            row[6] = row[2] ** self.w_freq * \
                     row[3] ** self.w_monogram * \
                     row[4] ** self.w_bigram * \
                     row[5] ** self.w_trigram
        with open("data.csv", "w+", newline='') as my_csv:
            csvWriter = csv.writer(my_csv, delimiter=',')
            csvWriter.writerows(self.data)
        # generate words
        self.search_words()
        self.choosewords()
        self.printselected()
        self.letterpos = 0
        self.nextletter = self.printline[self.letterpos]
        # update labels
        self.ent_type.delete(0, 'end')
        self.txt_words.delete("1.0", tk.END)
        self.txt_words.insert(END, self.printline)
        self.cleanmonogram = [[k, int(float(v))] for k, v in self.monogram.items() if
                              any(k in word for word in self.wordlist)]
        self.lbl_monogram2.config(text=sorted(self.cleanmonogram, key=itemgetter(1), reverse=True)[:5])
        self.lbl_monogram.config(
            text="Worst monograms (" + str(len([v for k, v in self.cleanmonogram if v == 2000])) + ")")
        self.cleanbigram = [[k, int(float(v))] for k, v in self.bigram.items() if
                            any(k in word for word in self.wordlist)]
        self.lbl_bigram2.config(text=sorted(self.cleanbigram, key=itemgetter(1), reverse=True)[:5])
        self.lbl_bigram.config(
            text="Worst bigrams (" + str(len([v for k, v in self.cleanbigram if v == 4000])) + ")")

        self.cleantrigram = [[k, int(float(v))] for k, v in self.trigram.items() if
                             any(k in word for word in self.wordlist)]

        self.lbl_trigram2.config(text=sorted(self.cleantrigram, key=itemgetter(1), reverse=True)[:4])
        self.lbl_trigram.config(
            text="Worst trigrams (" + str(len([v for k, v in self.cleantrigram if v == 6000])) + ")")
        self.oldscore = self.score
        self.score1 = stat.mean([v for k, v in self.cleanmonogram])
        self.score2 = stat.mean([v for k, v in self.cleanbigram])
        self.score3 = stat.mean([v for k, v in self.cleantrigram])
        self.score = int((self.score1 * self.score2 * self.score3) / (10 ** 6))
        self.scorediff = int(self.score - self.oldscore)
        self.lbl_score2.config(text=str(self.score) + " (" + str(self.scorediff) + ")")
        # update action_record
        if self.oldlen > 0:
            self.action_record.append(
                [tm.time_ns(), self.oldlen, int(self.score1), int(self.score2), int(self.score3), int(self.score),
                 int(self.scorediff)])
        self.plot()
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
        self.action_record = []
        for row in self.data:
            row[3] = row[4] = row[5] = 1
        self.txt_words.delete("1.0", tk.END)
        self.txt_words.insert(END, "RESET RECORDS")

    def key_pressed(self, event):
        if event.char == self.nextletter and self.ent_type.get() == self.printline[:self.letterpos + 1]:
            self.letterpos += 1
            letter_time = (tm.time_ns() - float(self.record[-1][1])) / (10 ** 6)
            if (letter_time > 2000 or self.letterpos == 1) and event.char != " ":
                letter_time = float(self.monogram[event.char])
            letter_wpm = 0.66 * 12 * (10 ** 3) / letter_time
            ema_wpm = 0.01 * letter_wpm + 0.99 * float(self.record[-1][4])
            self.record.append([event.char, tm.time_ns(), letter_time, letter_wpm, ema_wpm])
            self.monogram |= {k: 0.02 * letter_time + 0.98 * float(self.monogram[k])
                              for k in self.monogram if k == event.char}
            bigram_time = letter_time * 2
            self.bigram |= {k: 0.1 * bigram_time + 0.9 * float(self.bigram[k])
                            for k in self.bigram if k == str(self.record[-2][0] + event.char)}
            trigram_time = (letter_time + float(self.record[-2][2])) * 1.5
            self.trigram |= {k: 0.2 * trigram_time + 0.8 * float(self.trigram[k])
                             for k in self.trigram if k == str(self.record[-3][0] + self.record[-2][0] + event.char)}
            self.lbl_wpm2.config(text=int(ema_wpm))
        self.nextletter = self.printline[self.letterpos]
        self.txt_words.delete("1.0", tk.END)
        self.txt_words.insert(END, self.printline[:self.letterpos], "done")
        self.txt_words.insert(END, self.printline[self.letterpos:])
        if self.letterpos == len(self.printline) - 1:
            self.action(event=1)


def main():
    root = Tk()
    root.title("Smart Typer v2.1")
    window = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
