from heapq import heappush, heappop, heapify
import collections
from collections import defaultdict
from tkinter import *
import math
from graphviz import Digraph


def buildTree(event):
    try:
        dot.render('tree.gv', view=True)
    except:
        raise Exception("Please close the file before generating tree.")

def setupWindow():
    # Setting up windows
    encodedMessageLabel.grid(row=3, column=0, sticky='w')
    resultEntry.grid(row=4, column=0)
    nonEncodedLabel.grid(row=3, column=2, sticky='w')
    resultEntry2.grid(row=4, column=2)
    freq1Label.grid(row=5, column=0, sticky='w')
    freq2Label.grid(row=5, column=2, sticky='w')
    resultLabel.grid(row=6, column=0, sticky='w')
    test.grid(row=7, column=0, sticky='w')
    seeTreeButton.grid(row=2, column=2, sticky='w')

    # Deleting previous values
    resultEntry.config(state=NORMAL)
    resultEntry.delete(1.0, END)
    resultEntry2.config(state=NORMAL)
    resultEntry2.delete(1.0, END)


def formatString(event):
    setupWindow()
    str1 = str(inputString.get())
    if ".txt" in str1:
        try:
            file = open(str1, 'r')
            str1 = ""
            for line in file:
                str1 = str1 + line.strip()
        except:
            raise Exception("File path does not exist.")

    symb2freq = collections.Counter(str1)
    prevtotal = getFrequencies(symb2freq)

    global huff
    huff = encode(symb2freq)

    # Insert in window
    resultEntry.insert(INSERT, "Character\tFrequency\tCode\n")
    total = 0
    for p in huff:
        resultEntry.insert(INSERT, "   %s\t    %s\t     %s\n" % (p[0], symb2freq[p[0]], p[1]))
        total += len(p[1]) * symb2freq[p[0]]
        for i in str1:
            str1 = str1.replace(p[0], p[1])
    file2 = open('result.txt', 'w')
    file2.write(str1)
    efficiency = total/prevtotal * 100

    freq1LabelVar.set('Total bits = %s' % total)
    resultVar.set('Efficiency = %.2f' % efficiency + '%')
    #  prints huffman code in file
    testVar.set('Coded message => see result.txt')
    #  prints huffman code in window, not fitted
    #  testVar.set('Coded message = %s' % str1)

def getFrequencies(inputCnt):
    codeLength = math.ceil(math.log(len(inputCnt), 2))
    c = 0
    total = 0
    resultEntry2.insert(INSERT, "Character\tFrequency\tCode\n")
    for key, val in inputCnt.most_common():
        st = ('{0:b}'.format(c)).zfill(codeLength)
        resultEntry2.insert(INSERT,"   %s\t    %s\t     %s\n" % (key, val, st))
        c += 1
        total += val * len(st)
    freq2LabelVar.set('Total bits = %s' % total)
    return total

def encode(symb2freq):

    global dot
    dot = Digraph(comment='Huffman encoding tree')

    c = 65
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]

    heapify(heap)


    nodestack = {}

    while len(heap) > 1:
        added = 0
        lo = heappop(heap)
        hi = heappop(heap)

        dot_lo = str(lo[0]) + ' | ' + str(lo[1][0])
        dot_hi = str(hi[0]) + ' | ' + str(hi[1][0])

        orc = (chr(c))
        dot.node(chr(c), str(lo[0] + hi[0]))
        nodestack[chr(c)] = lo[0] + hi[0]
        c += 1

        if lo[0] not in nodestack.values():
            dot.node(chr(c), dot_lo)
            dot_lo_c = chr(c)
            nodestack[chr(c)] = lo
            c += 1
            added += 1
        else:
            for k, v in nodestack.items():
                if v == lo[0]:
                    dot_lo_c = k
                    break

        if hi[0] not in nodestack.values():
            dot.node(chr(c), dot_hi)
            dot_hi_c = chr(c)
            nodestack[chr(c)] = hi
            added += 1
        else:
            for k, v in nodestack.items():
                if v == hi[0]:
                    dot_hi_c = k
                    break



        # extra edges added just to add the labelzz
        dot.edge(orc, dot_lo_c, label='0')
        dot.edge(orc, dot_hi_c, label='1')


        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
        c += 1
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def buildWindow():
    root = Tk()

    global encodedMessageLabel, nonEncodedLabel, freq1LabelVar, \
           freq2LabelVar, resultVar, resultEntry, resultEntry2, \
           freq1Label, freq2Label, resultLabel, inputString, seeTreeButton, \
           test, testVar

    welcomelabel = Label(root, text="Enter the message to encode or path of .txt:")
    welcomelabel.grid(row=1, column=0)

    inputString = Entry(root, width=50)
    inputString.grid(row=2, column=0)


    submitButton = Button(root, text="Submit")
    submitButton.bind("<Button-1>", formatString)
    submitButton.grid(row=2, column=1, sticky='w')

    seeTreeButton = Button(root, text="Generate tree")
    seeTreeButton.bind("<Button-1>", buildTree)

    freq1LabelVar = StringVar()
    freq2LabelVar = StringVar()
    resultVar = StringVar()
    testVar = StringVar()

    encodedMessageLabel = Label(root, text="Encoded Message:")
    nonEncodedLabel = Label(root, text="Non huffman encoding:")
    freq1Label = Label(root, textvariable=freq1LabelVar)
    freq2Label = Label(root, textvariable=freq2LabelVar)
    resultLabel = Label(root, textvariable=resultVar)
    test = Label(root, textvariable=testVar)

    resultEntry = Text(root, height=12, width=33)
    resultEntry2 = Text(root, height=12, width=33)

    root.mainloop()

# aaaaabbbbbbbbbccccccccccccdddddddddddddeeeeeeeeeeeeeeeefffffffffffffffffffffffffffffffffffffffffffff
# AAAAAAAAAAEEEEEEEEEEEEEEEIIIIIIIIIIIISSSTTTTPPPPPPPPPPPPP
buildWindow()
