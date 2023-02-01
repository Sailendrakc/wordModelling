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
    iterations = utilities.sampleGroupForXdaysNTimes(xdays, bookPath, booksPerDay, convoPath, convoPerDay, iterationTime)
    #FinalList is an array, that contain item called dobj, dobj has attributes : day ( which day), totalWordCount, uniqueWordcount, averaged (true if the data is averaged ntimes).
    print('sampling done');
    #[[day1, day2, day3, day4, day4], [day1, day2, day3, day4], [day1, day2, day3, day4]]

    averagedIterationCycle = utilities.averageIteration(iterations)
    #[AvgDay1, AvgDay2, AvgDay3, AvgDay4]

    #defecit iterations
    defecitIteration = utilities.defecitIteration(iterations, 10)
    #[[_day1, _day2, _day3, _day4], [_day1, _day2, _day3, _day4], [_day1, _day2, _day3, _day4]]

    #Create average cycle out of defecit iterations.
    averagedDefecitIterationCycle = utilities.averageIteration(defecitIteration)
    #[_AvgDay1, _AvgDay2, _AvgDay3, _AvgDay4]

    # get plotting data and plot for each data points.
    utilities.graphCycleData([averagedIterationCycle, averagedDefecitIterationCycle], True, False);

test_sampleForXdaysNTimes()
