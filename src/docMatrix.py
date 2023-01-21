
import pandas as pd # Install pandas for this
import os
import string
from sklearn.feature_extraction.text import CountVectorizer # Install scikit-learn package for this.
# Also install openpyxl.


#This method is used to remove whitespaces and punctuation from a string and it returns a list of words.
def line_tokenizer(line: str, punctuationDict: dict = None) -> list:

    punc = punctuationDict
    if punctuationDict is None:
        punc = str.maketrans('','', string.punctuation)

        # Remove apostrophie from make trans dictionary so it wont be translated to None.
        apostrophieUnicode = 39
        del punc[apostrophieUnicode]

    wordList =  line.lower().strip(" '").translate(punc).split()

    for i in range(len(wordList)):
        wordList[i] = wordList[i].strip(" '")

    return wordList


def ToDocumentMatrix(path):
        if(type(path) is not str):
             raise Exception("document Path should be string")

        if path is None or not os.path.exists(path):
            raise Exception("Please provide a valid path.")

        df1 = None

        # Open file and read the excel corpus as dataframe
        try:
            df1 = pd.read_excel(path)
            del df1[df1.columns[0]]
        except Exception as e:
            print(e)
            print("Error reading the excel file")
            return

        #Get list of actual words to make matrix of.
        rawWordList = df1["Randomized Tokens"].values.tolist()

        print(df1)
        print("\n ----------------------------------------------- \n")

        #pncuation
        punc = str.maketrans('','', string.punctuation)
        # Remove apostrophie from make trans dictionary so it wont be translated to None.
        apostrophieUnicode = 39
        del punc[apostrophieUnicode]

        #Vectoried it
        #https://stackoverflow.com/questions/61023227/countvectorizer-splitting-on-space-instead-of-on-comma
        vectorizer = CountVectorizer(tokenizer=lambda text: line_tokenizer(text, punc))
        vectorized_matrix = vectorizer.fit_transform(rawWordList)
        names = vectorizer.get_feature_names_out()
        dataa = vectorized_matrix.todense()

        #Create new dataframe
        df2 = pd.DataFrame(data =dataa, columns = names, index = df1["Transcript_FILE_ID"])
        df2 = df2.reset_index()

        print("\n ----------------------------------------------- \n")

        # Get Transpose coz excel limit
        print(df2.shape)
        df2 = df2.T
        df2.replace(0, None, inplace=True)
        print(df2)
        #Now save dataframe as csv
        print(" \nSaving the matrix document, Please dont close the program, It may take a while... \n")
        df2.to_csv("vectorizedDoc.csv")
        print("Document saved, Now you can close the program.")

pathtofile = r'C:\Users\saile\OneDrive\Desktop\wordModelling\otherSrc\rawPreDTM.xlsx'
ToDocumentMatrix(pathtofile)