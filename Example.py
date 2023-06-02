#!/usr/bin/env python

# if installed using pip
from tt_wizard_core import tt_wizard_core

# if not installed using pip and using source code
# from src.tt_wizard_core import tt_wizard_core

print("Welcome to an example of TT_WIZARD_CORE!")

# Create an tt_wizard_core object and provide it with the path to your pen,
# otherwise the current directory is used.
# A list of all available media files is downloaded automatically.
print("What is the path to your TipToi pen?")
penPath = str(input())
ttwiz = tt_wizard_core(penPath)
if len(penPath) < 1:
    penPath = ""
    ttwiz = tt_wizard_core()

# Provide a string to search in the list of available media . 
print("Please enter keyword to search avaiable media for: ")
keyword = str(input())

# Search for string and receive a python list of media titles that partially match.
print("Found following media:")
searchResult = ttwiz.searchEntry(keyword)
num = 0
for item in searchResult:
    print(str(num) + ": " + item)
    num = num + 1

# Decide on which one to download and download media to folder specified in first step.
print("Which one do you like to download?")
chosenNum = int(input())
ttwiz.downloadMedium(searchResult[chosenNum]) #searchResult[chosenNum] is "<<fileName>>.gme"

# Pass the path and file name to retrieve information on whether an update is suggested or not.
print("Update? " + str(ttwiz.checkForUpdate(penPath, searchResult[chosenNum])))