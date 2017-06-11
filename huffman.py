from heapq import heappush, heappop, heapify
import collections
from collections import defaultdict
from tkinter import *
import math


def setupWindow():
    # Setting up windows
    encodedMessageLabel.grid(row=3, column=0, sticky='w')
    resultEntry.grid(row=4, column=0)
    nonEncodedLabel.grid(row=3, column=2, sticky='w')
    resultEntry2.grid(row=4, column=2)
    freq1Label.grid(row=5, column=0, sticky='w')
    freq2Label.grid(row=5, column=2, sticky='w')
    resultLabel.grid(row=6, column=0, sticky='w')

    # Deleting previous values
    resultEntry.config(state=NORMAL)
    resultEntry.delete(1.0, END)
    resultEntry2.config(state=NORMAL)
    resultEntry2.delete(1.0, END)


def formatString(event):
    setupWindow()
    str1 = str(inputString.get())
    symb2freq = collections.Counter(str1)
    prevtotal = getFrequencies(symb2freq)

    huff = encode(symb2freq)

    # Insert in window
    resultEntry.insert(INSERT, "Character\tFrequency\tCode\n")
    total = 0
    for p in huff:
        resultEntry.insert(INSERT, "  %s\t  %s\t  %s\n" % (p[0], symb2freq[p[0]], p[1]))
        total += len(p[1]) * symb2freq[p[0]]

    freq1LabelVar.set('Total bits = %s' % total)
    resultVar.set('Efficiency = %s' % (total/prevtotal))


def getFrequencies(inputCnt):
    codeLength = math.ceil(math.log(len(inputCnt), 2))
    c = 0
    total = 0
    resultEntry2.insert(INSERT, "Character\tFrequency\tCode\n")
    for key, val in inputCnt.most_common():
        st = ('{0:b}'.format(c)).zfill(codeLength)
        resultEntry2.insert(INSERT,"  %s\t  %s\t  %s\n" % (key, val, st))
        c += 1
        total += val * len(st)
    freq2LabelVar.set('Total bits = %s' % total)
    return total

def encode(symb2freq):
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def buildWindow():
    root = Tk()

    global encodedMessageLabel, nonEncodedLabel, freq1LabelVar, \
           freq2LabelVar, resultVar, resultEntry, resultEntry2, \
           freq1Label, freq2Label, resultLabel, inputString

    welcomelabel = Label(root, text="Enter the message to encode:")
    welcomelabel.grid(row=1, column=0)

    inputString = Entry(root, width=50)
    inputString.grid(row=2, column=0)


    submitButton = Button(root, text="Submit")
    submitButton.bind("<Button-1>", formatString)
    submitButton.grid(row=2, column=1, sticky='w')

    seeTreeButton = Button(root, text="Generate tree")
    seeTreeButton.bind("<Button-1>", formatString)
    seeTreeButton.grid(row=2, column=2, sticky='w')

    freq1LabelVar = StringVar()
    freq2LabelVar = StringVar()
    resultVar = StringVar()

    encodedMessageLabel = Label(root, text="Encoded Message:")
    nonEncodedLabel = Label(root, text="Non huffman encoding:")
    freq1Label = Label(root, textvariable=freq1LabelVar)
    freq2Label = Label(root, textvariable=freq2LabelVar)
    resultLabel = Label(root, textvariable=resultVar)

    resultEntry = Text(root, height=12, width=33)
    resultEntry2 = Text(root, height=12, width=33)

    root.mainloop()

# aaaaabbbbbbbbbccccccccccccdddddddddddddeeeeeeeeeeeeeeeefffffffffffffffffffffffffffffffffffffffffffff
# AAAAAAAAAAEEEEEEEEEEEEEEEIIIIIIIIIIIISSSTTTTPPPPPPPPPPPPP
buildWindow()