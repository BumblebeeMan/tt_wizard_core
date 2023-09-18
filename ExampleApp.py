#!/usr/bin/env python

def searchEntry(mediaList: list, searchString: str):
    """ 
    Search available media files for specified keyword.

    param: >>searchString<< -- String. Keyword to be searched in available titles.
    return: a.) [] -- Empty list if string is NOT found in any title.
            b.) [] -- List of all titles that include >>searchString<<
    """
    result = []
    for item in mediaList:
        if searchString.upper() in item.upper():
            result.append(item)
    return result

# if installed using pip
#from tt_wizard_core import tt_wizard_core

# if not installed using pip and using source code
from src.tt_wizard_core import tt_wizard_core

print("Welcome to an example of TT_WIZARD_CORE!")

# Create an tt_wizard_core object and try to auto dectect pen
# A list of all available media files is downloaded automatically.
ttwiz = tt_wizard_core()
if ttwiz.autoDetectPenMountPoint() is False:
    # If pen is not detected automatically, set mount point manually.
    print("What is the path to your TipToi pen?")
    ttwiz.setPenMountPoint(str(input()))

# Get list of available titles
titleList = ttwiz.getAllAvailableTitles()

titleAsList = []
while True:
    # Provide a string to search in the list of available media. 
    print("Please enter keyword to search avaiable media for: ")
    keyword = str(input())
    
    # Search for string and receive a python list of media titles that partially match.
    print("Found following media:")
    searchResult = searchEntry(titleList, keyword)
    
    # Decide on which one to download and download media to folder specified in first step.
    if len(searchResult) >= 1:
        num = 0
        for item in searchResult:
            print(str(num) + ": " + item)
            num = num + 1
        print("Which one do you like to download?")
        chosenNum = int(input())
        if chosenNum >= 0 and chosenNum <= num:
            titleAsList.append(searchResult[chosenNum]) #searchResult[chosenNum] is "<<fileName>>.gme"
        else:
            print(f"Error! You picked {chosenNum}. Which is not within range 0 till {num}.")
            print("Please try again!")
    else:
        print(f"No titles containing \"{keyword}\" found.")
    
    print("Do you want do pick more files? [Y]/N ")
    option = str(input())
    if option == "N":
        break

print("You picked: " + str(titleAsList))
print("Do you want to download those files? [N]/Y")
option = str(input())
if option == "Y":
    print("Start downloading files...")
    ttwiz.downloadMedia(titleAsList) 
    print("Finished downloading files!")
