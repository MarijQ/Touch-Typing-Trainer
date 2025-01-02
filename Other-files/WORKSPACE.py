import csv

with open('data2.csv') as csvfile:
    data = list(csv.reader(csvfile, delimiter=","))
    data[0][0] = "the"

wordlist = [row[0] for row in data]
trigram = [[]]

for word in wordlist:
    print(word)
    for i in range(2, len(word)):
        newtg = word[i - 2] + word[i - 1] + word[i]
        if [newtg] not in trigram:
            trigram.append([newtg])

print(trigram)

with open("trigram2.csv", "w+", newline='') as my_csv:
    csvWriter = csv.writer(my_csv, delimiter=',')
    csvWriter.writerows(trigram)
