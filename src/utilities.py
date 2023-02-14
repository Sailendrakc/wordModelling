
from ast import Try
from cProfile import label
from cmath import e
from email import iterators
from pickle import TRUE
from dumpObject import dobj
import os
import glob
import random
import re
import math
import string
import matplotlib.pyplot as plt
import pandas as pd 
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')
nltk.download('omw-1.4')

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

        #Raw words is the list that contains all the words from file
        wordSet.rawWords = []

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
                wordSet.rawWords.append(word_list_from_line)
                wordSet.totalWordCount += len(word_list_from_line)
                uniqueWordSet.update(word_list_from_line)

        wordSet.uniqueWordCount = len(uniqueWordSet)
        wordSet.uniqueWordSet = uniqueWordSet
        # Return the set
        return wordSet

#This method is used to remove whitespaces and punctuation from a string and it returns a list of words.
def refineLine(line: str, punctuationDict: dict = None, normalize = False) -> list:

    punc = punctuationDict
    if punctuationDict is None:
        punc = str.maketrans('','', string.punctuation)

        # Remove apostrophie from make trans dictionary so it wont be translated to None.
        apostrophieUnicode = 39
        del punc[apostrophieUnicode]

    wordList =  line.lower().strip("' ").translate(punc).split()
    if normalize:
        normalizedList = []
        for word in wordList:
            normalizedList.append(wordnet_lemmatizer.lemmatize(word))
        return normalizedList

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

    # This function samples any group for certain amount of days.
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
        raise Exception("there are no enough content to sample. one of the given folder is empty.")

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
        notEnough = False

        while tempNewConvo > 0:
            newList.append(listofConvo[convoPointer])
            convoPointer += 1
            tempNewConvo -=1
            if convoPointer == convoLen:
                notEnough = True
                print('Not enought conversation to sample, sampling whatever content was left')
                break

        while tempNewBooks > 0:
            newList.append(listofBooks[bookPointer])
            bookPointer += 1
            tempNewBooks -= 1
            if bookPointer == bookLen:
                notEnough = True
                print('Not enought book to sample, sampling whatever content is left')
                break
        
        if notEnough:
            return graphData

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
        raise Exception("N times should be greater than 0")

    #[[day1, day2,day3 ...dayn], [day1, day2,day3 ...dayn], [day1, day2,day3 ...dayn]]
    iterations = []
    while nTimes > 0:
        print("Sampling for " + str(nTimes) + " th iteration.")
        oneIteration = sampleGroupForXdays(xdays, bookFolderPath, newBooks, convoFolderPath, newConvo)
        print(str(nTimes) + " th iteration sampled.")
        iterations.append(oneIteration)
        nTimes -=1

    return iterations


#This fucntion takes the iteration data and average it.
def averageIteration(iterationObject):

    if(len(iterationObject)< 1):
        raise Exception("iteration object has no items, canot average empty iteration data.")

    #If there is only one item, no need to average it, just return it.
    if(len(iterationObject) == 1):
        return iterationObject[0]

    #now average the data
    divisor = len(iterationObject)
    averagedGraphData =[]
    print('calculating the average ....')
    counter = 0
    xdays = len(iterationObject[0])

    while counter < xdays:
        graphObj = dobj()
        graphObj.day = counter +1
        graphObj.averaged= True
        graphObj.totalWordCount = 0
        graphObj.uniqueWordCount = 0

        for item in iterationObject:

            graphObj.totalWordCount += item[counter].totalWordCount
            graphObj.uniqueWordCount += item[counter].uniqueWordCount


        graphObj.totalWordCount = math.ceil(graphObj.totalWordCount/divisor)
        graphObj.uniqueWordCount = math.ceil(graphObj.uniqueWordCount/divisor)

        print("day is: " + str(counter+1) + " avg totalWordCount : " + str(graphObj.totalWordCount) + " avg unique word count : " + str(graphObj.uniqueWordCount))
        averagedGraphData.append(graphObj)
        counter +=1

    print("Finished calculating average")
    return averagedGraphData

# This function will defecit a sample by provided percentage.
def defecitASample(sampleObj, defecitPercentage):

    if isinstance(defecitPercentage, int):
        defecitPercentage = float(defecitPercentage)

    if isinstance(defecitPercentage, float) == False:
        raise Exception("defecitPercentage should be a number/float")

    if defecitPercentage < 0:
        raise Exception("defecit percentage should be a positive float")


    # TODO Also check samleObj.uniqueWordSet is not null etc, validate the data.

    #Create a list from word set and randomize it, (inorder to remove some random items and create a defecit)
    listFromSet = list(sampleObj.uniqueWordSet)
    random.shuffle(listFromSet)

    #Number of items to to remove from the sample data
    numberOfItems = math.floor((defecitPercentage/100) * len(listFromSet))

    newList = listFromSet[numberOfItems:]

    #Return new sample data with removed/reduced word set and unique word count.
    newSample = dobj()

    newSample.uniqueWordSet = set(newList)
    newSample.uniqueWordCount = len(newList)

    newSample.totalWordCount = len(listFromSet)

    newSample.day = sampleObj.day
    newSample.wordsRemoved = True

    return newSample

# This function will make a defecit to the iteration data by a given percentage.
def defecitIteration(iteration, defecitPercentage):
    iterationLen = len(iteration)
    if iterationLen < 1:
        raise Exception("Cannot defecit iteration with no data.")

    #Loop the iteration and make a defecit on each sample. Save the list of that sample to new Iteration list
    print("starting doing defecit to a iteration")
    newIteration = []
    for simulation in iteration:
        newsimulation = []
        for sample in simulation:
            newSample = defecitASample(sample, defecitPercentage)
            newsimulation.append(newSample)
            print("Deficit done for a simulation")
        print("defecit done to an iteration.")
        newIteration.append(newsimulation)

    return newIteration

# This function will graph a simulation(list of [daily samples, label]) or list of simulations.
# All simulations should have equal number of samplings in them. 
def graphsimulationData(simulationDataList, plot = False, saveasCSV= False, savingFileName = 'graphData.csv'):
    if simulationDataList == None or len(simulationDataList) < 1:
        raise Exception("Please pass a valid simulation data list to plot")
    print("Graphing data")
    #Prepare data
    days = None
    try:
        days = range(1, len(simulationDataList[0][0]) + 1)
    except:
        raise Exception("Please put valid data and label for graphing. It should be a list of list like, [[graphngdata1, lable1], [graphingdata2, label2]]." +
            "Labels should not be same")

    plt.xlabel('Days')
    plt.ylabel('Words')

    fieldsForCSV = {}

    for simulations in simulationDataList:
        dailyUniqueWordCountList =[]
        dailyTotalWordCountList = []

        for sample in simulations[0]:
            dailyUniqueWordCountList.append(sample.uniqueWordCount)
            dailyTotalWordCountList.append(sample.totalWordCount)
        _label = ''
        try:
           _label = simulations[1]
        except:
            raise Exception("Please put valid label for graphing. It should be a list of list like, [[graphngdata1, lable1], [graphingdata2, label2]]." +
            "Labels should not be same and should start with an alphabet and not like '_dog' ")
        if saveasCSV:
            fieldsForCSV[_label] = dailyUniqueWordCountList
        #Plot
        if plot:
            print(_label)
            plt.plot(days, dailyUniqueWordCountList, label = _label) #or use totalWords to plot total words 
            plt.legend(loc="upper left")
    
    if plot:
        plt.show()

    #Save as csv
    if saveasCSV:
        # dictionary of lists  
        df = pd.DataFrame(fieldsForCSV) 
        # saving the dataframe 
        df.to_csv(savingFileName) 
        print(savingFileName + " file saved!")


#This function takes a baseline iteration and adds new books and conversation to each sample.
def addBookAndConvoToIteration(bookFolderPath, newBooks, convoFolderPath, newConvo, iteration):
    listofBooks = getAllBookPath(bookFolderPath)
    listofConvo = getAllBookPath(convoFolderPath)

    random.shuffle(listofBooks)
    random.shuffle(listofConvo)

    bookLen = len(listofBooks)
    convoLen = len(listofConvo)

    bookPointer = 0
    convoPointer = 0


    if bookLen == 0 or convoLen == 0:
        raise Exception("there are no enough content to sample. one of the given folder is empty.")
    if iteration == None or len(iteration) == 0:
        raise Exception("the iteration is null. Cannot add new books and conversation when baseline iteration is null or invalid.")

    xdays = len(iteration[0])
    totalRequiredBooks = xdays * newBooks
    totalRequiredConvo = xdays * newConvo

    if totalRequiredBooks > bookLen:
        print(str(totalRequiredBooks) + " books are necessary for sampling but only availabe books are: " + str(bookLen) +
       ". Warning, further sampling will be discontinued and final result will be caculated as is. ")

    if totalRequiredConvo > convoLen:
       print(str(totalRequiredConvo) + " conversations are necessary for sampling but only availabe conversations are: " + str(convoLen) +
       ". Warning, further sampling will be discontinued and final result will be caculated as is. ")

    newIteration = []
    for simulation in iteration:
        newsimulation = []
        lastSample = None
        for sample in simulation:
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
            # Sample baseline sampling and todays sampling
            mixedSampling = sampleTwoSamplings(newSampling, sample)
            finalSampling = sampleTwoSamplings(mixedSampling, lastSample)
            lastSample = finalSampling
            newsimulation.append(finalSampling)
            print("baseline sample enriched sucessfully.")

        newIteration.append(newsimulation)
        print("new books and convo added to a baseline simulation.")
    return newIteration
