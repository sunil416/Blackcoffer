from doctest import master
from numpy import iscomplex
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os
from pathlib import Path
import nltk
from nltk.tokenize import word_tokenize,sent_tokenize
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


from InputReader import InputReader
class DataExtractor:
    
    #Constructor 
    def __init__(self) -> None:
        try:
            #installs the chrome driver
            self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        except Exception as e:
            print(f"Exception occured at DataExtractor Constructor {e}")
    
    def openUrl(self, url):
        try:
            if self.driver:
                self.driver.get(url)
        except Exception as e:
            print(f"Exception at opening URL {e}")
    
    def findElementByClassName(self, atical_path):
        #element= self.driver.find
        element= self.driver.find_element_by_class_name(atical_path)
        return element

class ReadFile:
    def __init__(self, path,fileName, fileextension) -> None:
        self.fileName=fileName
        self.path= path
        self.fileExtension= fileextension
        
    def ReadFile(self, endcoding):
        try:
            lines=[]
            filepath= Path(f"{self.path}\\{self.fileName}{self.fileExtension}")
            with open(filepath,"r", encoding=endcoding) as f:
                line=f.readline()
                while line != "":
                    if line[-2:] == "\n":
                        lines.append(line[:-2])
                    else:
                        lines.append(line)
                    line =f.readline()
            return lines  
        except Exception as e:
            print(f"Exception occurenred while reading the path { self.path} ,file {self.fileName} , extension {self.fileExtension}, exception {e}")
    

def ExtractData():
    cwd = os.getcwd()
    print(f"Path = {cwd}")
    input=InputReader("Code\Input.xlsx")
    print(f"input read succfully with size{input.data.shape}")
    urlsList=input.data["URL"]
    extractor_obj=DataExtractor()
    for url in urlsList:
        print(f"Reading URl {url}")
        if url != NULL and url !="":
            extractor_obj.openUrl(url)
            data= extractor_obj.findElementByClassName("td-post-content")
            print(f"Data Extracted for Urls {url}\n")
            output_file = Path(cwd+f"\\Code\\Data\\{url[8:-2]}.txt")
            output_file.parent.mkdir(exist_ok=True, parents=True)
            with open(output_file,"w",encoding="utf-8") as f:
                f.writelines(data.text)
                print(f"Data Written in the files successfully")
def CleanData(current_path):
        
        print("current path ="+current_path)
        current_path=Path(current_path+"\\Code\\StopWords")
        files=os.listdir(current_path)
        stopWordList=[]
        for file in files:
            #print(file[len(file)-3:])
            print(file)
            filename= file[:-4]
            extension= file[len(file)-4:]
            if  extension== ".txt":
                readfile= ReadFile(current_path, filename, extension)
                data=readfile.ReadFile("unicode-escape")
                stopWordList.extend(data)
        #print(stopWordList)
        #print(cleanData(" ",stopWordList))
        cleanWords=[]
        for word in stopWordList:
            splited_words= word.split(" ")
            cleanWords.append(splited_words[0].strip())
        return cleanWords

def CleanTheArticleWithStopWord(current_path, stopWords):

    input_path= Path(current_path+"\Code\Data\insights.blackcoffer.com")
    output_path= Path(f"{current_path}\Code\Data\StopWordRemovedData")
    files=os.listdir(input_path)
    for file in files:
        print(file)
        filename= file[:-4]
        extension= file[len(file)-4:]
        if  extension== ".txt":
            readfile= ReadFile(input_path, filename, extension)
            lines=readfile.ReadFile("utf-8")
            newlines =[]
            if lines is not None:
                for line in lines:
                    newLine=""
                    splited_words=line.split(" ")
                    for word in splited_words:
                        if( word.lower() not in stopWords) or(word.upper() not in stopWords) or (word not in stopWords):
                            newLine=newLine+" "+word
                    newlines.append(newLine)
                output_file=Path(f"{output_path}\{filename}{extension}")
                print("-------------------------Writing the file-------------------")
                print(f"Path = {output_path}")
                with open(output_file,"w",encoding="utf-8") as f:
                    f.writelines(newlines)
                    print(f"Data Written in the files successfully")    

'''Read and creats a dictionary of postive words'''

def ReadandCreatePostiveWordDictionary(current_Path, stop_Words):

    input_Path= current_Path#Path(f"{current_Path}\Code\MasterDictionary\positive-words.txt")
    posotive_words=[]
    with open(input_Path, "r") as f:
        line= f.readline()
        while line != "":
            word=line.strip().upper()
            isWordFound= False
            for stop_word in stop_Words:
                if stop_word.upper() == word:
                    isWordFound= True
            
            if not isWordFound:
                posotive_words.append(word)

            line= f.readline()
    return posotive_words

'''
function used to return the list of the tokens from the given file path
'''
def GetTokensForTheInputStream(file_Path):
    list_of_tokens=[]
    total_no_of_lines=0
    with open( file_Path, "r", encoding="utf-8") as f:
        line= f.readline()
        
        while line != "":
            #total_no_of_lines+=1
            #tokens=word_tokenize(line, preserve_line=True)
            total_no_of_lines+=len(sent_tokenize(line))
            tokenizer = RegexpTokenizer(r'\w+')
            tokens=tokenizer.tokenize(line)
            #print(tokens)
            list_of_tokens.extend(tokens)
            line= f.readline()
    
    return (list_of_tokens,total_no_of_lines)

def CalculatePostiveAndNegativeScore(base_path,master_dict):
    file_parent_path=f"{base_path}\StopWordRemovedData"
    files=os.listdir(file_parent_path)
    dict_for_number_of_line={}
    average_number_of_words_per_sentance={}
    for file in files:
        filename= file[:-4]
        extension= file[len(file)-4:]
        if extension== ".txt":
            outputFile_Path= Path(f"{base_path}\Tokens\{filename}.csv")
            out=GetTokensForTheInputStream(Path(f"{file_parent_path}\\{file}"))
            total_valid_token= CalculatePostiveScore(outputFile_Path,out[0], master_dict )
            dict_for_number_of_line.update({filename:out[1]})
            average_number_of_words_per_sentance.update({filename:(round(len(total_valid_token)/out[1]))})
    #print(dict_for_number_of_line) 
    #print(average_number_of_words_per_sentance)    

    POSITIVE_SCORE=[]
    NEGATIVE_SCORE=[]
    Polarity_Score=[]
    Subjectivity_Score=[]
    PERCENTAGE_OF_COMPLEX_WORDS=[]
    FOG_INDEX=[]
    COMPLEX_WORD_COUNT=[]
    WORD_COUNT=[]
    SYLLABLE_PER_WORD=[]
    AVG_WORD_LENGTH=[]
    URL=[]
    files=os.listdir(f"{base_path}\Tokens")
    for file in files:
        filename= file[:-4]
        extension= file[len(file)-4:]
        if extension== ".csv":
            input_Path= Path(f"{base_path}\Tokens\{filename}.csv")
            temp_da= pd.read_csv(input_Path)
            POSITIVE_SCORE.append(temp_da[temp_da["Score"]==1].sum()["Score"])
            NEGATIVE_SCORE.append(temp_da[temp_da["Score"]==-1].sum()["Score"]*-1)
            #Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
            Polarity_Score.append((POSITIVE_SCORE[-1]-NEGATIVE_SCORE[-1])/((POSITIVE_SCORE[-1]+NEGATIVE_SCORE[-1])+ 0.000001))
            #Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
            Subjectivity_Score.append((POSITIVE_SCORE[-1]+NEGATIVE_SCORE[-1])/((temp_da.shape[0])+ 0.000001))
            #Percentage of Complex words = the number of complex words / the number of words 
            PERCENTAGE_OF_COMPLEX_WORDS.append(temp_da[temp_da["IsComplex"]==1].shape[0]/temp_da.shape[0])

            #Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
            FOG_INDEX.append(0.4*(PERCENTAGE_OF_COMPLEX_WORDS[-1]+average_number_of_words_per_sentance[filename]))

            COMPLEX_WORD_COUNT.append(temp_da[temp_da["IsComplex"]==1].shape[0])

            WORD_COUNT.append(temp_da.shape[0])

            SYLLABLE_PER_WORD.append(temp_da["Syllable_Count"].sum())
            AVG_WORD_LENGTH.append(calcualte_average_wordLenght(input_Path))
            URL.append(filename)
    finnal_data_frame=pd.DataFrame()
    finnal_data_frame["File_Name"]= URL
    finnal_data_frame["POSITIVE_SCORE"]= POSITIVE_SCORE
    finnal_data_frame["NEGATIVE_SCORE"]= NEGATIVE_SCORE
    finnal_data_frame["Polarity_Score"]= Polarity_Score
    finnal_data_frame["Subjectivity_Score"]= Subjectivity_Score
    finnal_data_frame["Average_Sentence_Length"]= average_number_of_words_per_sentance.values()
    finnal_data_frame["PERCENTAGE_OF_COMPLEX_WORDS"]= PERCENTAGE_OF_COMPLEX_WORDS
    finnal_data_frame["FOG_INDEX"]= FOG_INDEX
    finnal_data_frame["AVG_NUMBER_OF_WORDS_PER_SENTENCE"]= average_number_of_words_per_sentance.values()
    finnal_data_frame["COMPLEX_WORD_COUNT"]= COMPLEX_WORD_COUNT
    finnal_data_frame["WORD_COUNT"]= WORD_COUNT
    finnal_data_frame["SYLLABLE_PER_WORD"]= SYLLABLE_PER_WORD
    finnal_data_frame["AVG_WORD_LENGTH"]= AVG_WORD_LENGTH

    finnal_data_frame.to_csv(f"{base_path}\\Output_Data.csv")


    #data_frame.to_csv(outputFile_Path)

def calcualte_average_wordLenght(filePath):

    data=pd.read_csv(filePath)
    words_list=data["Token"]
    count =0
    for word in words_list:
        count+=len(word)
    return round(count/len(words_list))


def CalculatePostiveScore(file_name, tokens, master_Dictionary):

    postive= master_Dictionary["Postive"]
    negative= master_Dictionary["Negative"]
    nltk_stopWords=[w.strip().upper() for w in stopwords.words('english')]
    tokeValue=[]
    temp_token=[]
    sylabee_Count=[]
    word_lenght=[]
    isComplex=[]
    for tok in tokens:
        if tok.strip().upper() not in nltk_stopWords:
            temp_token.append(tok)

    for token in temp_token:
        word=token.strip().upper()
        sylabbe=Calculate_Sylabee(word)
        sylabee_Count.append(sylabbe)
        isComplex.append( 1 if sylabbe>2 else 0)
        word_lenght.append(len(word))
        if word in postive:
            tokeValue.append(1)
        elif word in negative:
            tokeValue.append(-1) 
        else :
            tokeValue.append(0) 
    dataframe= pd.DataFrame(index=None)
    dataframe["Token"]= temp_token
    dataframe["Score"]= tokeValue
    dataframe["Syllable_Count"]= sylabee_Count
    dataframe["Word_length"]= word_lenght
    dataframe["IsComplex"]= isComplex

    dataframe.to_csv(file_name)
    return temp_token

def Calculate_Sylabee(word):

    vovles=['a','e','i','o','u']
    count =0
    if word.strip().lower().endswith("es") or word.strip().lower().endswith("ed"):
        return count

    for letter in word:
        if letter.strip().lower() in vovles:
            count+=1
    return count



if __name__=="__main__":
    current_path=os.getcwd()
    ExtractData()

    print("\n------------------Reading Stop Words Started-----------------------\n")
    StopWords=CleanData(current_path)
    print("\n------------------Reading Stop Words Completed-----------------------\n")

    print("\n ------------------ Cleaning the files using stop words started --------------------\n")
    CleanTheArticleWithStopWord(current_path, StopWords)
    print("\n ------------------ Cleaning the files using stop words Completed --------------------\n")
    master_Dictionary= {}
    print("\n ------------------ Creating Postive Word Dictionary started --------------------\n")
    
    master_Dictionary.update({"Postive": ReadandCreatePostiveWordDictionary(Path(f"{current_path}\Code\MasterDictionary\positive-words.txt"), StopWords)})
    print("\n ------------------ Creating Postive Word Dictionary Completed --------------------\n")

    print("\n ------------------ Creating Negative Word Dictionary started --------------------\n")
    master_Dictionary.update({"Negative": ReadandCreatePostiveWordDictionary(Path(f"{current_path}\Code\MasterDictionary\\negative-words.txt"), StopWords)})
    print("\n ------------------ Creating Negative Word Dictionary Completed --------------------\n")

    #print(master_Dictionary)
    # once time activity 
    nltk.download('punkt')
    nltk.download('stopwords')
    print("\n ------------------ Creating Token started --------------------\n")
    CalculatePostiveAndNegativeScore((Path(f"{current_path}\Code\Data")), master_Dictionary)

    print("\n ------------------ Creating Token Ended --------------------\n")
