import utilities
import random
import re

inFolder = r'C:\Users\saile\OneDrive\Desktop\wordModelling\childesRAW'
outFolder = r'C:\Users\saile\OneDrive\Desktop\wordModelling\cleanChildes'

# This function take a folder containing conversations and outputs the folder that has files containing word spoken by child only. 
# one input file == 1 conversation == 1 output file.
def cleaner(inputFolder, outFolder, subfiles):
    listOfTxtFiles =  utilities.getAllFilePath(inputFolder, subfiles, '.cha')
    print(listOfTxtFiles)

    #now open them line by line and clean it and put in outfut folder.
    for filee in listOfTxtFiles:
        childLineToFile(filee, outFolder)

# This function extracts the line spoken by child in a conversation and writes an output file for it.
def childLineToFile(path, outFolder = outFolder):
    with open(path, "r", encoding = 'utf-8') as file1:
        print(".Opening File: " + path + "\n")
        exposedWords = ''
        ageStr = ''
        for line in file1:
            if ageStr == '' and line.startswith('@ID:') and 'CHI' in line:
                ageStr = line.split('|')[3].replace(';', 'Y').replace('.', 'M')
                ageStr += 'D'
                
            if line.startswith('*'):
                words = re.sub(r'[^a-zA-Z\s]', '', line).split()# split the sentence into words
                if(len(words) == 0):
                    continue
                cleanLine = " ".join(words[1:])
                if cleanLine == '':
                    continue
                exposedWords += cleanLine + '\n'
    

        if(ageStr == ''):
            print("Cannot extract age for: " + path)
            return
        if exposedWords.strip() == '':
            print("Empty convo, ignoring..")
            return
        #Make a file out of childWords
        newFileName = outFolder + "/"+ ageStr + "_"+str(random.randint(1000, 10000))+ ".txt"
        with open(newFileName, "w", encoding = 'utf-8') as outfile:
            outfile.write(exposedWords)
        print("... One convo extracted ... \n")
        
    
cleaner(inFolder, outFolder, True)