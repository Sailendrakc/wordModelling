
from ast import Try
from cmath import e
from dumpObject import dobj
import os
import glob
import random
import re
import math
import string
import matplotlib.pyplot as plt
import pandas as pd 

# this function returns token, typecount and type set ( unique word list) from a  text file file
def readTxtData(path: str) -> dobj:
        
        if(type(path) is not str):
             raise Exception("Some paths in lists are not valid path. Path should be string")

        if path is None or not os.path.exists(path):
            raise Exception("Please provide a valid path.")

        #Object to store text attributes like token, types and unique word set
        wordSet = dobj()
        wordSet.totalWordCount = 0
        wordSet.uniqueWordCount = 0
        uniqueWordSet = set()

        # Open file
        with open(path, "r") as file1:

            #Create a dictionary to replae the punctuation from the sentence.
            punc = str.maketrans('','', string.punctuation)

            # Remove apostrophie from make trans dictionary so it wont be translated to None.
            apostrophieUnicode = 39
            del punc[apostrophieUnicode]

            # Read and extract into a set
            for line in file1:
                word_list_from_line = refineLine(line, punc)
                wordSet.totalWordCount += len(word_list_from_line)
                uniqueWordSet.update(word_list_from_line)

        wordSet.uniqueWordCount = len(uniqueWordSet)
        wordSet.uniqueWordSet = uniqueWordSet
        # Return the set
        return wordSet

#This method is used to remove whitespaces and punctuation from a string and it returns a list of words.
def refineLine(line: str, punctuationDict: dict = None) -> list:

    punc = punctuationDict
    if punctuationDict is None:
        punc = str.maketrans('','', string.punctuation)

        # Remove apostrophie from make trans dictionary so it wont be translated to None.
        apostrophieUnicode = 39
        del punc[apostrophieUnicode]

    wordList =  line.lower().strip("' ").translate(punc).split()
    return wordList



# this function gets all the .txt files inside a given folder
def getAllBookPath(pathOfFolder: str) -> list:
        if pathOfFolder is None or not os.path.exists(pathOfFolder):
            raise Exception("Please provide a valid path.")

        # Load a random file from the folder.

        files = glob.glob(pathOfFolder + "/*.txt")
        poolOfFiles = []
        # loop through list of files
        for f in files:
            poolOfFiles.append(f)

        return poolOfFiles


# this function takes a list of txt files and samples it.
def SampleConversation(paths : list) -> dobj:
        # read all the files and sample them

        subSample = []

        for path in paths:
            subSample.append(readTxtData(path))

        #Now subsample contains word count and unique word count ( number of token and types)
        #We can caluclate average or whatever from this data.

        finalsample = dobj()
        finalsample.uniqueWordSet = {}
        finalsample.totalWordCount = 0
        
        for elem in subSample:
            finalsample.totalWordCount += elem.totalWordCount
            finalsample.uniqueWordSet = set().union(finalsample.uniqueWordSet).union(elem.uniqueWordSet)

        finalsample.uniqueWordCount = len(finalsample.uniqueWordSet)

        return finalsample


def sampleGroupForXdays(xdays: int, bookFolderPath: str, newBooks: int, convoFolderPath:str, newConvo: int):
    
    listofBooks = getAllBookPath(bookFolderPath)
    listofConvo = getAllBookPath(convoFolderPath)

    random.shuffle(listofBooks)
    random.shuffle(listofConvo)

    lastSample = None
    graphData = []
    day = 1

    bookLen = len(listofBooks)
    convoLen = len(listofConvo)

    bookPointer = 0
    convoPointer = 0
    
    if bookLen == 0 or convoLen == 0:
        raise("there are no enough content to sample. one of the given folder is empty.")

    totalRequiredBooks = xdays * newBooks
    totalRequiredConvo = xdays * newConvo

    if totalRequiredBooks > bookLen:
        print(str(totalRequiredBooks) + " books are necessary for sampling but only availabe books are: " + str(bookLen) +
       ". Warning, further sampling will be discontinued and final result will be caculated as is. ")

    if totalRequiredConvo > convoLen:
       print(str(totalRequiredConvo) + " conversations are necessary for sampling but only availabe conversations are: " + str(convoLen) +
       ". Warning, further sampling will be discontinued and final result will be caculated as is. ")

    while day <= xdays:
        #Do the sampling.
        if bookPointer == bookLen or convoPointer == convoLen:
            break

        newList = []
        tempNewBooks = newBooks
        tempNewConvo = newConvo

        while tempNewConvo > 0:
            newList.append(listofConvo[convoPointer])
            convoPointer += 1
            tempNewConvo -=1
            if convoPointer == convoLen:
                print('Not enought conversation to sample, sampling whatever content was left')
                break

        while tempNewBooks > 0:
            newList.append(listofBooks[bookPointer])
            bookPointer += 1
            tempNewBooks -= 1
            if bookPointer == bookLen:
                print('Not enought book to sample, sampling whatever content is left')
                break
        
        newSampling = SampleConversation(newList)

        # Sample yesterday sampling and todays sampling
        finalSampling = sampleTwoSamplings(newSampling, lastSample)

        # this is daily data required for graphing
        graphObj = dobj()
        graphObj.day = day
        graphObj.totalWordCount = finalSampling.totalWordCount
        graphObj.uniqueWordCount = finalSampling.uniqueWordCount
        graphObj.uniqueWordSet = finalSampling.uniqueWordSet
        graphObj.averaged = False

        #print("day is: " + str(graphObj.day) + " totalWordCount : " + str(graphObj.totalWordCount) + " unique word count : " + str(graphObj.uniqueWordCount))

        graphData.append(graphObj)

        lastSample = finalSampling
        day += 1

    return graphData

def sampleTwoSamplings(sample1, sample2):

    if sample1 is None:
        return sample2

    if sample2 is None:
        return sample1
        
    finalsample = dobj()
    
    finalsample.totalWordCount = sample1.totalWordCount + sample2.totalWordCount
    finalsample.uniqueWordSet = set().union(sample1.uniqueWordSet).union(sample2.uniqueWordSet)
    finalsample.uniqueWordCount = len(finalsample.uniqueWordSet)

    return finalsample

def sampleGroupForXdaysNTimes(xdays: int, bookFolderPath: str, newBooks: int, convoFolderPath:str, newConvo:int, nTimes: int):
    if nTimes <= 0:
        raise("N times should be greater than 0")

    #[[day1, day2,day3 ...dayn], [day1, day2,day3 ...dayn], [day1, day2,day3 ...dayn]]
    iterations = []
    
    while nTimes > 0:
        oneIteration = sampleGroupForXdays(xdays, bookFolderPath, newBooks, convoFolderPath, newConvo)
        print(str(nTimes) + " th iteration done.")
        iterations.append(oneIteration)
        nTimes -=1

    divisor = len(iterations)
    averagedGraphData =[]
    #now average the data
    print('calculating the average ....')
    counter = 0
    while counter < xdays:
        graphObj = dobj()
        graphObj.day = counter +1
        graphObj.averaged= True
        graphObj.totalWordCount = 0
        graphObj.uniqueWordCount = 0
        graphObj.uniqueWordSet = set()

        for item in iterations:
            graphObj.totalWordCount += item[counter].totalWordCount
            graphObj.uniqueWordCount += item[counter].uniqueWordCount
            graphObj.uniqueWordSet  = set.union(graphObj.uniqueWordSet).union(item[counter].uniqueWordSet) # ----------------- TODO ASK

        graphObj.totalWordCount = math.ceil(graphObj.totalWordCount/divisor)
        graphObj.uniqueWordCount = math.ceil(graphObj.uniqueWordCount/divisor)

        print("day is: " + str(counter+1) + " avg totalWordCount : " + str(graphObj.totalWordCount) + " avg unique word count : " + str(graphObj.uniqueWordCount))
        averagedGraphData.append(graphObj)
        counter +=1


    return averagedGraphData

#This takes a list of sampling data from day1 to dayn, then removesx percentage of uniue words from the set.
def removeWordsFromUniqueSet(averagedData, percentage):
    if averagedData == None:
        raise("Please pass a valid averaged data")

    if percentage > 100 or percentage < 0:
        raise("Percentage of words to be removed should be between 0 to 100.")
    
    print("Removing some percentage of unique words")

    #now loop the data and remove x percentage of words.
    for n in range(len(averagedData)):
        item = averagedData[n]
        listFromSet = list(item.uniqueWordSet)
        random.shuffle(listFromSet)

        #now calculate how much items to remove
        numberOfItems = math.floor((percentage/100)*len(item.uniqueWordSet))

        newList = listFromSet[numberOfItems:]
        item.uniqueWordSet = set(newList)
        item.uniqueWordCount = len(item.uniqueWordSet)

    return averagedData

def graphAveragedData(averagedData, plot = False, saveasCSV= False):
    if averagedData == None:
        raise("Please pass a valid averaged data")

    #Prepare data
    days = range(1, len(averagedData) + 1)

    dailyUniqueWordCountList =[]
    dailyTotalWordCountList = []

    for dailyAverageData in averagedData:
        dailyUniqueWordCountList.append(dailyAverageData.uniqueWordCount)
        dailyTotalWordCountList.append(dailyAverageData.totalWordCount)

    #Plot
    if plot:
        plt.plot(days, dailyUniqueWordCountList) #or use totalWords to plot total words 
        plt.xlabel('Days')
        plt.ylabel('Words')
        plt.show()
    
    #Save as csv
    if saveasCSV:
        # dictionary of lists  
        fields = {'days': days, 'totalWords': dailyTotalWordCountList, 'uniqueWords': dailyUniqueWordCountList}  
       
        df = pd.DataFrame(fields) 
    
        # saving the dataframe 
        df.to_csv('wordModelling.csv') 

    return dailyUniqueWordCountList; #returning a list of numbers that represents unique word count in each day.
