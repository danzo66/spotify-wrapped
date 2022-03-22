from openpyxl import load_workbook
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import requests
import math

"""

basically put each person's wrapped into a different excel doc, 
save them all into one folder, the same as these files, 
and then put the file names into the variable files 
(make sure they're in quotes/apostrophes, and separated by commas)
 
I've copied and pasted this all from spotify so i had only urls instead of names
so i had to search the web for names
this takes a LONG FUCKING TIME, so if you have the actual names of the files in an excel doc
make sure you have fast set to True to skip all this 

allwrapped = loaddata(files, fast=True)  

sw = 21
aw = 195

"""

beth = "beth.xlsx"
charlie = "charlie.xlsx"
dan = "danwrapped.xlsx"
dan20 = "dan2020.xlsx"
dan19 = "dan2019.xlsx"
dave = "dave.xlsx" 
harvey = "harvey.xlsx"
howard = "howard.xlsx"
mom = "mom.xlsx"
robbie = "robbie.xlsx"
ron = "ron.xlsx"
rory = "rory.xlsx"
sarah = "sarah.xlsx"
tabby = "tabby.xlsx"

def loaddata(file, fast):
    wb = load_workbook(filename=file)
    sheet = wb.active
    invwrapped = []
    for i in range(2,103):
        j = int(i)-2
        song = sheet["B"+str(i)].value
        if i == 2:
            print(str(sheet["B"+str(2)].value))
            print("Loading: " + str(j) + "%")
        if fast == False:
            if str(song) != "None":
                if song[0:4] == "http":
                    url = song[0:4] + song[5:]
                    response = requests.get(url)
                    txt = response.text
                    title = txt[txt.find('<title>') + 7 : txt.find('</title>')]
                    song = title[0:-10]
                    if j%5 == 4:
                        print(str(sheet["B"+str(2)].value))
                    elif j%5 == 0:
                        print("Loading: " + str(j) + "%")
                    else:
                        print(".")
        invwrapped.append(song)
    np.save(str(invwrapped[0]) + ".npy", invwrapped, allow_pickle = True)
    return invwrapped
    
fist = [beth]

for i in fist:
    allwrapped = loaddata(i, fast=False)  