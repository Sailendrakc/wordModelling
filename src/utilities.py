
from xml.dom.minidom import Element
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
from sklearn.feature_extraction.text import CountVectorizer # Install scikit-learn package for this.

#Lemetizer and Stemmer
wordnet_lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()

nltk.download('wordnet')
nltk.download('omw-1.4')

# this function returns token, typecount and type set ( unique word list) from a  text file file
def readTxtData(path: str, lemmatize) -> dobj:
        
        if(type(path) is not str):
             raise Exception("Some paths in lists are not valid path. Path should be string")

        if path is None or not os.path.exists(path):
            raise Exception("Please provide a valid path.")

        #Object to store text attributes like token, types and unique word set
        wordSet = dobj()
        wordSet.totalWordCount = 0
        wordSet.uniqueWordCount = 0

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
                word_list_from_line = refineLine(line, punc, lemmatize)
                wordSet.rawWords.extend(word_list_from_line)

        wordSet.uniqueWordSet = set(wordSet.rawWords)
        wordSet.uniqueWordCount = len(wordSet.uniqueWordSet)
        wordSet.totalWordCount = len(wordSet.rawWords)

        # Return the set
        return wordSet

#This method is used to remove whitespaces and punctuation from a string and it returns a list of words.
# If lemmatize is set to false, the words will be stemmized, as default, lemmatize is set to true.
def refineLine(line: str, punctuationDict: dict = None, lemmatize = None) -> list:

    punc = punctuationDict
    if punctuationDict is None:
        punc = str.maketrans('','', string.punctuation)

        # Remove apostrophie from make trans dictionary so it wont be translated to None.
        apostrophieUnicode = 39
        del punc[apostrophieUnicode]

    wordList =  line.lower().strip("' ").translate(punc).split()
    if lemmatize == None:
        return wordList
    else:
        if lemmatize:
            lemmatizeList = []
            for word in wordList:
                lemmatizeList.append(wordnet_lemmatizer.lemmatize(word))
            return lemmatizeList
        else:
            stemmizedList = []
            for word in wordList:
                stemmizedList.append(porter_stemmer.stem(word))
            return stemmizedList

# this function gets all the .txt files inside a given folder
def getAllFilePath(pathOfFolder: str, recursive = False ,extension = '.txt') -> list:
        if pathOfFolder is None or not os.path.exists(pathOfFolder):
            raise Exception("Please provide a valid path.")

        extensionString = "/*"+ extension
        if recursive:
            extensionString = "/**" + extensionString

        files = glob.glob(pathOfFolder + extensionString, recursive = recursive)
        poolOfFiles = []
        # loop through list of files
        for f in files:
            poolOfFiles.append(f)

        return poolOfFiles


# this function takes a list of txt files and samples it.
def SampleConversation(paths : list, lemitize = None, stoplist = {}) -> dobj:
        # read all the files and sample them

        subSample = []

        for path in paths:
            subSample.append(readTxtData(path, lemitize))

        #Now subsample contains word count and unique word count ( number of token and types)
        #We can caluclate average or whatever from this data.

        finalsample = dobj()
        finalsample.uniqueWordSet = {}
        finalsample.totalWordCount = 0
        finalsample.inputs = paths;
        finalsample.allWordList = []

        
        for elem in subSample:
            finalsample.allWordList.extend(elem.rawWords)

        finalsample.allWordList = [word for word in finalsample.allWordList if word not in stoplist]
        finalsample.uniqueWordSet = set(finalsample.allWordList)    #.difference(set(stoplist))
        finalsample.uniqueWordCount = len(finalsample.uniqueWordSet)
        finalsample.totalWordCount  = len(finalsample.allWordList)

        return finalsample

    # This function samples any group for certain amount of days.
def sampleGroupForXdays(xdays: int, bookFolderPath: str, newBooks: int, convoFolderPath:str, newConvo: int):
    
    listofBooks = getAllFilePath(bookFolderPath)
    listofConvo = getAllFilePath(convoFolderPath)

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

        #create the df for exposure count
        newSampling.matrixDf = pd.DataFrame('Day', 'transcipt')
        newSampling.matrixDf.append({'Day':day, 'transcipt': newSampling.allWordString}, ignore_index = True)

        #Vectorize it.
        vectorizer = CountVectorizer()
        rawWordList = newSampling.matrixDf["transcipt"].values.tolist()
        vectorized_matrix = vectorizer.fit_transform(rawWordList)
        names = vectorizer.get_feature_names_out()
        dataa = vectorized_matrix.todense()
        df2 = pd.DataFrame(data =dataa, columns = names, index = newSampling.matrixDf["Day"])
        df2 = df2.T
        df2.replace(0, None, inplace=True)
        newSampling.matrixDf = df2

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

    #Also combine the dataframe.
    if hasattr(sample1, 'matrixDf') and hasattr(sample2, 'matrixDf') == False:
        finalsample.matrixDf = sample1.matrixDf

    if hasattr(sample2, 'matrixDf') and hasattr(sample1, 'matrixDf') == False:
        finalsample.matrixDf = sample2.matrixDf

    if hasattr(sample1, 'matrixDf') and hasattr(sample2, 'matrixDf'):
        finalsample.matrixDf = pd.merge(sample1.matrixDf, sample2.matrixDf, left_index=True, right_index=True, how='outer')
        finalsample.matrixDf = finalsample.matrixDf.fillna(0)
        finalsample.matrixDf = finalsample.matrixDf.astype(int)

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

#This function takes a sample to enrich and list of txt files path to enrich from , then returns enriched sample.
def enrichSample(originalSample, listOfSrcToEnrichFrom):
    newDataSample = SampleConversation(listOfSrcToEnrichFrom)
    enrichedSample = sampleTwoSamplings(originalSample, newDataSample)
    enrichedSample.log = " "
    enrichedSample.log += "These inputs were used in enriching:" + "\n"
    for links in listOfSrcToEnrichFrom:
            enrichedSample.log += "    " + links + "\n"
    enrichedSample.log = "Inputs for enrich had types: " + str(newDataSample.totalWordCount) + " tokens (unique): " + str(newDataSample.uniqueWordCount) + "\n"
    return enrichedSample

def sampleToString(sample):
    return " TotalWords: " + str(sample.totalWordCount) + " uniqueWords: " + str(sample.uniqueWordCount)

#This function takes a baseline iteration and adds new books and conversation to each sample.
def addBookAndConvoToIteration(bookFolderPath, newBooks, convoFolderPath, newConvo, iteration):
    
    if newBooks <= 0 and newConvo <= 0:
        print("No new resources to add to iteration, hence returning original iteraiton.")
        return iteration


    listofBooks = getAllFilePath(bookFolderPath)
    listofConvo = getAllFilePath(convoFolderPath)

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

#This takes exposure dataframe and calculates on which day a token reached exposure threshold and appends it in new column.
def findAndAppendLearntDay(df, threshold):
    # Loop through each row and column in reverse order
    learntDay = []
    average = []
    realIndex = 0
    for index, row in df.iterrows():
        days = 0 
        rawThres = 0
        thresholdReached = False
        for column in reversed(df.columns):
            rawThres +=  row[column]
            days += 1
            if rawThres >= threshold:
                thresholdReached = True
                break
        if thresholdReached == True:
            learntDay.append(days)
        else:
            learntDay.append(0)

        row_list = row.values.tolist()
        del row_list[0]
        avg = sum(row_list) / len(row_list)
        average.append(avg);
        realIndex += 1

    df = df.assign(Learned_Day = learntDay)
    df = df.assign(avg_exposure_perDay = average)
    return df


# This method will take list of dataframes and combines them and averages the word count.
# Use this method to combine and average the result of exposure count matrix.
def dfUnion(dfList):
    mainMatrix = 0
    listLen = len(dfList)
    for i in range(listLen):
        elem = dfList[i]
        if i == 0:
            mainMatrix = elem
            continue
        else: 
            merged_df = pd.concat([mainMatrix, elem], axis='columns').fillna(0)
            merged_df = merged_df.groupby(level=0, axis=1).sum()
            mainMatrix = merged_df

    numeric_cols = mainMatrix.select_dtypes(include=['int', 'float']).columns
    #numeric_cols = mainMatrix.iloc[:, 1:]
    mainMatrix[numeric_cols] = mainMatrix[numeric_cols] / listLen

    return mainMatrix