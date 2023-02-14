import unittest
import utilities
import os
import shutil
from dumpObject import dobj

class TestUtilities(unittest.TestCase):

    def test_refineLineWithNormalization(self):
        testStr = " I am eating a lot of apples."
        expectedList = ['i', 'am', 'eating', 'a', 'lot', 'of', 'apple']
        outputList = utilities.refineLine(testStr, None, True)
        self.assertEqual(outputList, expectedList)

    def test_getAllBookPath(self):
        
        folderPath = os.getcwd() + "\\testFolder"
        
        #Create a folder with files
        os.mkdir(folderPath)

        with open('testFolder/testFile1.txt', 'w') as f:
            f.write('New Test File')

        with open('testFolder/testFile2.txt', 'w') as f:
            f.write('New Test File')

        with open('testFolder/testFile3.docs', 'w') as f:
            f.write('New Test File docs')

        expectedResult = [folderPath+'\\testFile1.txt',
                        folderPath+'\\testFile2.txt']
        unexpectedResult1 = [folderPath+'\\testFile1.txt',
                        folderPath+'\\testFile2.txt',
                        folderPath+'\\testFile3.docs']
        result = utilities.getAllBookPath(folderPath)

        #Delete the created contents.
        shutil.rmtree(folderPath)

        self.assertEqual(result, expectedResult)
        self.assertNotEqual(result, unexpectedResult1)

    def test_sampleConversation(self):

        folderPath = os.getcwd() + "\\testFolder"
        
        #Create a folder with files
        os.mkdir(folderPath)

        with open('testFolder/testFile1.txt', 'w') as f:
            f.write('happy birthday to you and thank you very much birthday is always happy and never sad')

        with open('testFolder/testFile2.txt', 'w') as f:
            f.write('happy new year to you and you are very welcome')

        with open('testFolder/testFile3.txt', 'w') as f:
            f.write('happy marriage aniversary to you stay good stay fit and never sad')

        sampledResult = utilities.SampleConversation(utilities.getAllBookPath(folderPath))

        expectedUniqueWordSet = {'happy', 'birthday', 'to', 'you', 'and', 'thank', 'very', 'much', 'is', 'always', 'never', 'sad', 'new', 
                                 'year', 'are', 'welcome', 'marriage', 'aniversary', 'stay', 'good', 'fit'}
        expectedTotalWordCount = 38
        expectedUniqueWordCount = len(expectedUniqueWordSet)

        #Delete the created contents.
        shutil.rmtree(folderPath)

        self.assertIsNotNone(sampledResult)
        self.assertEqual(sampledResult.uniqueWordSet, expectedUniqueWordSet)
        self.assertEqual(sampledResult.totalWordCount, expectedTotalWordCount)
        self.assertEqual(sampledResult.uniqueWordCount, expectedUniqueWordCount)

    def test_readtextData(self):

        folderPath = os.getcwd() + "\\testFolder"
        
        #Create a folder with files
        os.mkdir(folderPath)
        textContent = '  Hey Hey hey How is it going is the summer going good I hope you enjoy your time    Sure I will enjoy this time Ok  '
        with open('testFolder/testFile1.txt', 'w') as f:
            f.write(textContent)

        sampledData = utilities.readTxtData(folderPath + '\\testFile1.txt')
        shutil.rmtree(folderPath)
        
        expectedTotalWordCount = 25
        expectedwordSet = {'hey','how', 'is', 'it', 'going', 'the', 'summer', 'good', 'i', 'hope', 'you', 'enjoy', 'your',
                           'time', 'sure', 'will', 'this', 'ok'}
        expectedTotalUniqueWordCount = len(expectedwordSet)

        self.assertIsNotNone(sampledData)

        self.assertEqual(sampledData.totalWordCount, expectedTotalWordCount)
        self.assertEqual(sampledData.uniqueWordCount, expectedTotalUniqueWordCount)
        self.assertTrue(sampledData.uniqueWordSet == expectedwordSet)

    def test_sampleTwoSamplings(self):

        folderPath = os.getcwd() + "\\testFolder"
        
        #Create a folder with files
        os.mkdir(folderPath)

        with open('testFolder/testFile1.txt', 'w') as f:
            f.write('apple ball cat ball apple')

        with open('testFolder/testFile2.txt', 'w') as f:
            f.write('lion zebra apple cat grass zoo')

        result = utilities.getAllBookPath(folderPath)

        sampledData1 = utilities.readTxtData(result[0])
        sampledData2 = utilities.readTxtData(result[1])

        finalSampling = utilities.sampleTwoSamplings(sampledData1, sampledData2)
        shutil.rmtree(folderPath)

        expectedSample = dobj()
        expectedSample.uniqueWordSet = {'apple', 'ball', 'cat', 'lion', 'zebra', 'grass', 'zoo'}
        expectedSample.totalWordCount = 11
        expectedSample.uniqueWordCount = len(expectedSample.uniqueWordSet);

        self.assertIsNotNone(finalSampling)
        self.assertTrue(finalSampling.uniqueWordSet == expectedSample.uniqueWordSet)
        self.assertEqual(finalSampling.uniqueWordCount, expectedSample.uniqueWordCount)
        self.assertEqual(finalSampling.totalWordCount, expectedSample.totalWordCount)

    def test_refineLine(self):
        testStr = "' 'I am a fox? Am    I    A Fox.., ? He'y ! 10%  \n       \n  newLine  \n"
        expectedList = ['i', 'am', 'a', 'fox', 'am', 'i', 'a', 'fox', "he'y", '10', 'newline']
        outputList = utilities.refineLine(testStr, None)

        self.assertEqual(expectedList, outputList)



if __name__ == '__main__':
    unittest.main()