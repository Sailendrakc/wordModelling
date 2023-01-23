import utilities
import os
import matplotlib.pyplot as plt
import pandas as pd 


def plotDailyData(dailyData, dailyData2 = None):

    days = range(1, len(dailyData) + 1)
    plt.plot(days, dailyData)

    if dailyData2 != None:
        plt.plot(days, dailyData2)

    plt.xlabel('Days')
    plt.ylabel('Words')
    plt.show()


def test_sampleForXdaysNTimes():
    bookPath = r'C:\Users\saile\OneDrive\Desktop\wordModelling\Books'
    convoPath = r'C:\Users\saile\OneDrive\Desktop\wordModelling\Convos'

    xdays = 365
    booksPerDay = 0
    convoPerDay = 3
    iterationTime = 5

    print('Starting the sampling..')
    finalList = utilities.sampleGroupForXdaysNTimes(xdays, bookPath, booksPerDay, convoPath, convoPerDay, iterationTime)
    #FinalList is an array, that contain item called dobj, dobj has attributes : day ( which day), totalWordCount, uniqueWordcount, averaged (true if the data is averaged ntimes).
    

    #Example on how to get unique word count list from graph data for plotting.
    uniqueWordCountList1 = utilities.graphAveragedData(finalList)
    #Now you can plot uniqueWordCountList however you like.

    removedUniqueWordData = utilities.removeWordsFromUniqueSet(finalList, 10)

    removedUniqueWordCountList = utilities.graphAveragedData(removedUniqueWordData)

    plotDailyData(uniqueWordCountList1, removedUniqueWordCountList)



test_sampleForXdaysNTimes()
