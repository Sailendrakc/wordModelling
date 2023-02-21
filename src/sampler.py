
from dumpObject import dobj
import utilities
import random
import math

# -----------OPTIONS ------------
# First we provide the necessary options to run
# This is the full path to the folder where books as .txt files are stored
bookFolderPath = r'C:\Users\saile\OneDrive\Desktop\wordModelling\Books'

#This is the full path to the folder where convo as .txt files are stored
convoFolderPath = r'C:\Users\saile\OneDrive\Desktop\wordModelling\Convos'

#This is the number of books to feed the child per day
booksPerDayForBaseline = 2

#This is the number of convos to feed the child per day
convoPerDayForBaseline = 0

# This is the number of days per one simulation.
totalDaysPerSimulation =10

# This is the number of simulation per iteration. All iterations data are averaged.
totalSimulationPerIteration = 5

# This is the percentage of defecit we are applying for simulation, it is a float data type.
defecitPercentage = 10

# Number of books to use to enrich vocab per day 
enrichBooksPerDay = 1

# Number of convos to use to enrich vocab per day
enrichConvoPerDay = 0

# This flag if set to true will print averaged numbers to the console.
printAveragedNumbers = True

# This flag will turn stemming on instead of lemitization if set to FALSE, default is true.
lemitize = True

#------------ PRORAM VARIABLES -----------#

# This stores the list of simulations that are sampled using above options



# ----------- INPUT VALIDATION -----------#
# For now validation will be part of the function that takes that input.

def sampleGroupForXdays():

    #Get all books and convo that are to be used for sampling
    listOfBooks =  utilities.getAllBookPath(bookFolderPath)
    listOfConvos = utilities.getAllBookPath(convoFolderPath)

    #Randomize the list
    random.shuffle(listOfBooks)
    random.shuffle(listOfConvos)

    #Sampling variables
    day = 1
    bookLen = len(listOfBooks)
    convoLen = len(listOfConvos)
    bookPointer = 0
    convoPointer = 0

    lastBaseSample = None
    lastDefecitSample = None
    lastEnrichedSample = None

    baseSimulation = []
    defecitSimulation = []
    enrichedSimulation = []

    #Now Start Sampling books and apply all options per sampling.
    while day <= totalDaysPerSimulation:
        #Do the sampling.
        if bookPointer == bookLen or convoPointer == convoLen:
            break

        #To store a list of books and convo files to perform base sampling
        newBaseList = []
        tempNewBooks = booksPerDayForBaseline
        tempNewConvos = convoPerDayForBaseline

        #To store a list of books and convo files to perform enrichment.
        newEnrichList = []
        tempNewEnrichBooks = enrichBooksPerDay
        tempNewEnrichConvos = enrichConvoPerDay

        notEnough = False

        # Generate a list of books and convo files to perform base sampling
        while tempNewConvos > 0:
            newBaseList.append(listOfConvos[convoPointer])
            convoPointer += 1
            tempNewConvos -=1
            if convoPointer == convoLen:
                notEnough = True
                print('Not enought convo to sample, sampling wiil stop')
                break

        while tempNewBooks > 0:
            newBaseList.append(listOfBooks[bookPointer])
            bookPointer += 1
            tempNewBooks -= 1
            if bookPointer == bookLen:
                notEnough = True
                print('Not enought book to sample, sampling wiil stop')
                break

        # Generate a list of books and convo files to perform enrichment 
        while tempNewEnrichConvos > 0:
            newEnrichList.append(listOfConvos[convoPointer])
            convoPointer += 1
            tempNewEnrichConvos -=1
            if convoPointer == convoLen:
                notEnough = True
                print('Not enought convo to sample, sampling wiil stop')
                break

        while tempNewEnrichBooks > 0:
            newEnrichList.append(listOfBooks[bookPointer])
            bookPointer += 1
            tempNewEnrichBooks -= 1
            if bookPointer == bookLen:
                notEnough = True
                print('Not enought book to sample, sampling wiil stop')
                break
        
        if notEnough:
            break

        #Generate base sampling and then perform defit and enrichment on it.
        baseSampling = utilities.SampleConversation(newBaseList, lemitize)
        defecitSampling = utilities.defecitASample(baseSampling, defecitPercentage)
        enrichedSampling = utilities.enrichSample(defecitSampling, newEnrichList)

        # Sample yesterday sampling and todays sampling for all three kinds of samplings
        finalBaseSampling = utilities.sampleTwoSamplings(baseSampling, lastBaseSample)
        finalDefecitSampling = utilities.sampleTwoSamplings(defecitSampling, lastDefecitSample)
        finalEnrichedSampling = utilities.sampleTwoSamplings(enrichedSampling, lastEnrichedSample)

        lastBaseSample = finalBaseSampling
        lastDefecitSample = finalDefecitSampling
        lastEnrichedSample = finalEnrichedSampling

        print("sampling for day " + str(day) + " is done.")

        # Store all three kinds of samplings
        baseSimulation.append(finalBaseSampling)
        defecitSimulation.append(finalDefecitSampling)
        enrichedSimulation.append(finalEnrichedSampling)
        
        day += 1

    # Save the result as a sampling is complete.
    samplingResult = dobj()
    samplingResult.baseSimulation = baseSimulation
    samplingResult.defecitSimulation = defecitSimulation
    samplingResult.enrichedSimulation = enrichedSimulation

    return samplingResult

def SampleGroupForXDaysNTimes():

    # This list only stores average unique and total numbers as we are going to average n numbers of samples.
    baseIterationNumbers = []
    defecitIterationNumbers = []
    enrichedIterationNumbers = []

    ntimes = 0

    while ntimes < totalSimulationPerIteration:
        ntimes += 1
        simulationResult = sampleGroupForXdays()

        #Loop and average
        print(" \n" + str(ntimes) + " simulation done. \n")


        for days in range(0, totalDaysPerSimulation):

            if len(baseIterationNumbers) == days:

                # Creating objet to store uniqe and total words for each day 
                # for all three types of samplings and storing them to revalent list
                baseDobj = dobj()
                baseDobj.totalWordCount = 0
                baseDobj.uniqueWordCount = 0
                
                defecitDobj = dobj()
                defecitDobj.totalWordCount = 0
                defecitDobj.uniqueWordCount = 0

                enrichedDobj = dobj()
                enrichedDobj.totalWordCount = 0
                enrichedDobj.uniqueWordCount = 0

                baseIterationNumbers.append(baseDobj)
                defecitIterationNumbers.append(defecitDobj)
                enrichedIterationNumbers.append(enrichedDobj)

            #Adding all day1's and day2's .... dayN's unique and total word count together for all three sampling types.
            # We divide this total number by n times to calculate the average 

            #Example:

            # simulation 1 =    [day1        ,day2 ,       day3,         day4 ,       day5] #
            # simulation 2 =    [day1        ,day2 ,       day3,         day4 ,       day5] #
            # simulation 3 =    [day1        ,day2 ,       day3,         day4 ,       day5] #
            # simulation 4 =    [day1        ,day2 ,       day3,         day4 ,       day5] #
            # simulation 5 =    [day1        ,day2 ,       day3,         day4 ,       day5] #
            # ++(summation)=  ------------------------------------------------------------------

            #ITERATION Numbers =[Sum(day1's) ,sum(day2's) , sum(day3's), sum(day4's) ,sum(day5's)] #

            baseIterationNumbers[days].totalWordCount += simulationResult.baseSimulation[days].totalWordCount
            baseIterationNumbers[days].uniqueWordCount += simulationResult.baseSimulation[days].uniqueWordCount

            defecitIterationNumbers[days].totalWordCount += simulationResult.defecitSimulation[days].totalWordCount
            defecitIterationNumbers[days].uniqueWordCount += simulationResult.defecitSimulation[days].uniqueWordCount

            enrichedIterationNumbers[days].totalWordCount += simulationResult.enrichedSimulation[days].totalWordCount
            enrichedIterationNumbers[days].uniqueWordCount += simulationResult.enrichedSimulation[days].uniqueWordCount
    
    # Here we divide above summation to calculate average
    print("\n Averaging iterations \n")
    for dayx in range(0, totalDaysPerSimulation):
        baseIterationNumbers[dayx].totalWordCount = math.floor(baseIterationNumbers[dayx].totalWordCount / totalSimulationPerIteration)
        defecitIterationNumbers[dayx].totalWordCount = math.floor(defecitIterationNumbers[dayx].totalWordCount / totalSimulationPerIteration)
        enrichedIterationNumbers[dayx].totalWordCount = math.floor(enrichedIterationNumbers[dayx].totalWordCount / totalSimulationPerIteration)

        baseIterationNumbers[dayx].uniqueWordCount = math.floor(baseIterationNumbers[dayx].uniqueWordCount / totalSimulationPerIteration)
        defecitIterationNumbers[dayx].uniqueWordCount = math.floor(defecitIterationNumbers[dayx].uniqueWordCount / totalSimulationPerIteration)
        enrichedIterationNumbers[dayx].uniqueWordCount = math.floor(enrichedIterationNumbers[dayx].uniqueWordCount / totalSimulationPerIteration)
        
        if printAveragedNumbers:
            print("\n")
            print( "BASE: day is: " + str(dayx+1) + utilities.sampleToString(baseIterationNumbers[dayx]))
            print( "DEFECIT: day is: " + str(dayx+1) + utilities.sampleToString(defecitIterationNumbers[dayx]))
            print( "Enriched: day is: " + str(dayx+1) + utilities.sampleToString(enrichedIterationNumbers[dayx]))
            print("\n")

    #Now graph and save the simulations
    utilities.graphsimulationData([[baseIterationNumbers, "baseCurve"], [defecitIterationNumbers, "defecitCurve"], [enrichedIterationNumbers, "enrichedCurve"]], True)


SampleGroupForXDaysNTimes()