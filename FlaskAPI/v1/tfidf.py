import json
import csv
import math
from collections import OrderedDict
from operator import itemgetter

def computeTF(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    if bowCount == 0:
        return tfDict
    for word, count in wordDict.iteritems():
        tfDict[word] = count / float(bowCount)
        
    return tfDict

def computeIDF(docList):
    idfDict = {}
    N = len(docList)
    # N = 2
    #counts the number of documents that contain a word w
    idfDict = dict.fromkeys(docList[0].keys(),0)
    for doc in docList:
        for word, val in doc.iteritems():
            if val > 0:
                idfDict[word] += 1.0
                
    #divide N by denominator above, take the log of that
    for word, val in idfDict.iteritems(): 
      if val != 0:
        idfDict[word]= math.log(N / float(val)) 

    return idfDict

def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.iteritems():
        tfidf[word] = val * idfs[word]       
    return tfidf


def solve(reviews):   
    # Do Exception Handling!!! When no nouns match and tfidfMain is empty,bascially check if the dicts are not empty 
#====================Read Data====================== 
 with open('stopWords.csv', 'rb') as f:
  reader = csv.reader(f)
  inp2 = list(reader)
  StopWord = inp2[0]
   
 WordsDict = {}
 with open('polarity.csv', 'rb') as f:
  reader = csv.reader(f)
  WordList = list(reader)

 for row in WordList:
  WordsDict[str(row[1])] = (float(row[2]),row[0])

 with open('nouns.csv', 'rb') as f:
  reader = csv.reader(f)
  inp = list(reader)
 Nouns = inp[0]
 
 fname = "TestingDataForTFIDF.json"
 file_data = ""
 with open(fname, 'r') as fin:
  file_data = fin.read()
 data = json.loads(file_data)
#===============Start of Processing=================

 NounMain = {}
 
 punc = ",<>?/}{()*&^%$#@!\\"
 
 for i in range(len(reviews)):
  x = reviews[i].split('.')  
  for sentence in x:    
   arr = sentence.split(' ')
   for cstr in arr:
    if cstr not in punc:   
     p = str(cstr).lower()
     if p in Nouns and p not in StopWord and p != "it":
      NounMain[p] = 0
     
 #print "NounMain Length1 : " , len(NounMain) 
 
 WordMain = []
 BowMain = []

# Genearate Bag of Words and Dict
 for i in range(len(data['Reviews'])):
  x = data['Reviews'][i]['Content'].split('.')  
  bow = []
  nounRev = NounMain.copy()
  for sentence in x:    
   arr = sentence.split(' ')   
   for cstr in arr:
    p = str(cstr).lower()
    if p in NounMain and p not in StopWord and p != "it":
     bow.append(p)
     nounRev[p] += 1
  WordMain.append(nounRev)   
  BowMain.append(bow) 

 #print "BowMains: "
 #print (BowMain[0]),'\n',BowMain[1]
# print data['Reviews'][0]['Content']
 
 
# calculate TF-IDF
 
 tfBowMain = []

 for index in range(len(WordMain)):
     #if len(BowMain[index]) != 0:
         tfBowMain.append( ( computeTF( WordMain[index], BowMain[index]) ) ) 
 
 idfs = computeIDF(WordMain)
  
 tfidfMain = []
 
 for index in range(len(tfBowMain)):
     #if tfBowMain[index] != [None]:
      tfidfMain.append( ( computeTFIDF(tfBowMain[index], idfs) ) )
 
# Feature Selection via S.D.
 
 Sum = 0
 Count = 0

 #print d
 
 for i in range(len(tfidfMain)):
  for word, val in tfidfMain[i].iteritems():
    if val > 0:
        Sum += val
        Count += 1
 Avg = Sum/Count

 SD = 0
 
 for i in range(len(tfidfMain)):
  for word, val in tfidfMain[i].iteritems():
     if val > 0:
         SD += (val-Avg)**2
 SD /= Count
 SD = math.sqrt(SD)
 
 #print "Len of Data: ", len(data['Reviews'])

 #print "Average: ", Avg
 #print "SD: ", SD
 phi = 0
 #print '\n',"Phi ",phi,'\n'
# Features = []
 NewDict = {} 
# For features we have weights with which will plot Bar Graph, Features Weights Dict formation
 
 for i in range(len(reviews)):  
  for word, val in tfidfMain[i].iteritems():
     if  val > phi:
#      Features.append( (word,val) )
      NewDict[word] = max(0,val)
      
  d = OrderedDict(sorted(NewDict.items(), key=itemgetter(1),reverse=True))
#  print d
  
# Features.sort(key=lambda x: -x[1])

 print "\n\n ================ TF-IDF Score for Selected Features ================ \n\n"
 # select top 50. 
 i = 0;
 ret = {}
 
 for a in NewDict:
     i += 1
     if i < 50: 
         ret[a] = NewDict[a]
         print "  ", NewDict[a], " : ", a
     else:
        break
 
 return ret
 
print "Exec"


reviews = []
rev = "\"english teachers work native speakers languages thrilled flash cards. handsomely printed durable stock protective coating years shuffling. making twenty years result approached artful clear design sturdy compact cards. students linguistics find cards developing fluency ipa transcription.the transcription example english nice compromise overly broad unnecessarily narrow. diacritics example limited markers length syllabicity. general american accent model primary secondary stress marked syllable boundaries. esolefl teachers 43 cards covering sounds american english conveniently colorcoded deck 2 distinguish rest. linguistics students spend time decks symbol side its phonetic description reverse names individual symbols. decision separate decks package three decks generous wise: higher price capability accurately describe languages students hail south sudanone complain tool teaching sounds language sounds audibly. folks minokidowinan app iphone works task flashcards best suited improving fluency phonetic transcription written exercise. \""
reviews.append(rev)

#for i in range(len(data['Reviews'])):
# reviews.append( data['Reviews'][i]['Content'] )
    
solve(reviews)
