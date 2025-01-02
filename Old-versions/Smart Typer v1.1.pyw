import csv
from tkinter import *
import numpy as np
import time

global total_letters, start_time

with open('data.csv') as csvfile:
    data = list(csv.reader(csvfile, delimiter=","))
    data[0][0] = "the"


def isallowed(word, keylist, minsize):
    if len(word) < minsize:
        return False
    else:
        for letter in word:
            if letter not in keylist:
                return False
        return True


def search_words(data, keylist, minsize):
    activelist = []
    i = 0
    for word in data:
        if isallowed(word[0], keylist, minsize):
            activelist.append(word)
    return activelist


def choosewords(activelist, n):
    wordlist = [row[0] for row in activelist]
    freqlist = [int(row[1]) for row in activelist]
    freqsum = sum(freqlist)
    freqlist[:] = [n / freqsum for n in freqlist]
    selected = np.random.choice(a=wordlist, size=n, p=freqlist)
    return selected


def printselected(selected):
    printline = ""
    for word in selected:
        printline += str(word) + " "
    # print(sum([len(word) for word in selected]))
    return printline


def test():
    activelist = search_words(data, "qwertyuiopasdfghjklzxcvbnm", 3)
    selected = choosewords(activelist, 10)
    printline = printselected(selected)
    print(printline)


def main():
    global total_letters, start_time
    window = Tk()
    window.title("Smart Typer")

    global_font = ("Calibri", 30)
    global_width = 70

    lbl1 = Label(window, text="Allowed Letters: ", font=global_font)
    txt1 = Entry(window, width=global_width, font=global_font)
    txt1.insert(END, 'qwertyuiopasdfghjklzxcvbnm')

    lbl2 = Label(window, text="Minimum Word Size: ", font=global_font)
    txt2 = Entry(window, width=global_width, font=global_font)
    txt2.insert(END, '3')

    lbl5 = Label(window, text="Number of Words: ", font=global_font)
    txt5 = Entry(window, width=global_width, font=global_font)
    txt5.insert(END, '10')

    lbl3a = Label(window, text="Generated Words: ", font=global_font)
    lbl3b = Label(window, text="", font=global_font)

    lbl4 = Label(window, text="Type Here: ", font=global_font)
    txt4 = Entry(window, width=global_width, font=global_font)

    lbl5a = Label(window, text="Current WPM: ", font=global_font)
    lbl5b = Label(window, text="", font=global_font)

    total_letters = 0
    start_time = time.time()

    def clicked(event):
        global total_letters, start_time
        activelist = search_words(data, txt1.get(), int(txt2.get()))
        selected = choosewords(activelist, int(txt5.get()))
        printline = printselected(selected)
        lbl3b.config(text=printline)

        total_letters += len(txt4.get())
        total_time = time.time() - start_time
        WPM = total_letters / 5 / total_time * 60
        lbl5b.config(text=str(round(WPM)))

        txt4.delete(0, 'end')

    def reset(event):
        global total_letters, start_time
        total_letters = 0
        start_time = time.time()
        lbl5b.config(text="reset")

    window.bind('<Return>', clicked)
    window.bind('<Control-r>', reset)

    lbl1.grid(column=0, row=0)
    txt1.grid(column=1, row=0)
    lbl2.grid(column=0, row=1)
    txt2.grid(column=1, row=1)
    lbl5.grid(column=0, row=2)
    txt5.grid(column=1, row=2)
    lbl3a.grid(column=0, row=3)
    lbl3b.grid(column=1, row=3)
    lbl4.grid(column=0, row=4)
    txt4.grid(column=1, row=4)
    lbl5a.grid(column=0, row=5)
    lbl5b.grid(column=1, row=5)

    window.mainloop()


main()
