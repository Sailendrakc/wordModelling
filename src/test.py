import utilities
import os
import matplotlib.pyplot as plt
import pandas as pd 

def test_sampleForXdaysNTimes():
    bookPath = r'C:\Users\saile\OneDrive\Desktop\wordModelling\Books'
    convoPath = r'C:\Users\saile\OneDrive\Desktop\wordModelling\Convos'

    xdays = 365
    booksPerDay = 0
    convoPerDay = 5
    iterationTime = 10
    saveasCSV = False

    print('Starting the sampling..')
    finalList = utilities.sampleGroupForXdaysNTimes(xdays, bookPath, booksPerDay, convoPath, convoPerDay, iterationTime)
    #FinalList is an array, that contain item called dobj, dobj has attributes : day ( which day), totalWordCount, uniqueWordcount, averaged (true if the data is averaged ntimes).
    

    #Example on how to graph, not tested.

    #Prepare data
    days = range(1, xdays+1)
    totalWords = []
    uniqueWords =[]

    for dailyAverageData in finalList:
        totalWords.append(dailyAverageData.totalWordCount)
        uniqueWords.append(dailyAverageData.uniqueWordCount)
    
    #Plot
    plt.plot(days, uniqueWords) #or use totalWords to plot total words 
    plt.xlabel('Days')
    plt.ylabel('Words')
    plt.show()

    #Save as csv
    if saveasCSV:
        # dictionary of lists  
        fields = {'days': days, 'totalWords': totalWords, 'uniqueWords': uniqueWords}  
       
        df = pd.DataFrame(fields) 
    
        # saving the dataframe 
        df.to_csv('wordModelling.csv') 




test_sampleForXdaysNTimes()
