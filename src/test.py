from ctypes import util
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

    xdays = 10
    booksPerDay = 1
    convoPerDay = 0
    iterationTime = 5

    print('Starting the sampling..')

    #baseLine
    iterations = utilities.sampleGroupForXdaysNTimes(xdays, bookPath, booksPerDay, convoPath, convoPerDay, iterationTime)
    #FinalList is an array, that contain item called dobj, dobj has attributes : day ( which day), totalWordCount, uniqueWordcount, averaged (true if the data is averaged ntimes).
    print('sampling done');
    #[[day1, day2, day3, day4, day5], [day1, day2, day3, day4], [day1, day2, day3, day4]]

    averagedIterationsimulation = utilities.averageIteration(iterations)
    #[AvgDay1, AvgDay2, AvgDay3, AvgDay4]

    #defecit iterations
    defecitIteration = utilities.defecitIteration(iterations, 10)
    #[[_day1, _day2, _day3, _day4], [_day1, _day2, _day3, _day4], [_day1, _day2, _day3, _day4]]

    #Create average simulation out of defecit iterations.
    averagedDefecitIterationsimulation = utilities.averageIteration(defecitIteration)
    #[_AvgDay1, _AvgDay2, _AvgDay3, _AvgDay4]

    #this is iteration that was enriched with 1 book and 2 convo per day.
    #INPUT -[[_day1, _day2, _day3, _day4], [_day1, _day2, _day3, _day4], [_day1, _day2, _day3, _day4]]
    #OUTPUt - [[_day1, _day2, _day3, _day4], [_day1, _day2, _day3, _day4], [_day1, _day2, _day3, _day4]]
    addedIteration = utilities.addBookAndConvoToIteration(bookPath, 0, convoPath, 0, defecitIteration)

    #this is averaged version of that enriched iteration.
    averagedAddedIterationsimulation = utilities.averageIteration(addedIteration)

    # get plotting data and plot for each data points.
    utilities.graphsimulationData([averagedIterationsimulation, averagedDefecitIterationsimulation, averagedAddedIterationsimulation], True, False);

#test_sampleForXdaysNTimes()

def readBook():
    bookPath = r'C:\Users\saile\OneDrive\Desktop\wordModelling\Books'
    links =  utilities.getAllBookPath(bookPath)

    for x in range(0,6):
        path = links[x]
        print(path)
        res = utilities.readTxtData(path)
        print("total word count is : "+ str(res.totalWordCount) + " , unique word count is: " + str(res.uniqueWordCount))
        print("\n")

    #Noe read one by one
    #https://commentpicker.com/word-counter.php

readBook()