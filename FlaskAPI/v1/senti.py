import json
import csv
import math
from collections import OrderedDict
from operator import itemgetter

def solve(rev,rating):   
#====================Read Data======================
 print "Rating: ",rating
 rev = str(rev)
 rating = float(rating)
 
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
 
 print len(Nouns)
 
 negationWords = ["aint", "arent", "cannot", "cant", "couldnt", "darent", "didnt", "doesnt",
              "ain't", "aren't", "can't", "couldn't", "daren't", "didn't", "doesn't",
              "dont", "hadnt", "hasnt", "havent", "isnt", "mightnt", "mustnt", "neither",
              "don't", "hadn't", "hasn't", "haven't", "isn't", "mightn't", "mustn't",
              "neednt", "needn't", "never", "none", "nope", "nor", "not", "nothing", "nowhere",
              "oughtnt", "shant", "shouldnt", "uhuh", "wasnt", "werent",
              "oughtn't", "shan't", "shouldn't", "wasn't", "weren't",
              "without", "wont", "wouldnt", "won't", "wouldn't", "rarely", "seldom", "despite"]
 
 print "\n\n  ================ Sentiment Analysis Result ================ ", '\n'

 print "Processed Text:"
 print '\n',rev,'\n\n'
   
# Adjective and Noun Pairing
 FeatureDict = {} 
 avg = 0 
 cnt = 0
 #test = []
 # Fptr : Feature detected with index
 # Adjptr: Adjective detected with polarity and index
  
 for sentence in rev.split('.'):    
     Fptr = []
     AdjPtr = []     
     if sentence == '':
       continue                
     arr = sentence.split(' ')     
     i = 0
     direction = +1
     for cstr in arr:
       i += 1
       p = str(cstr).lower()
       if p in negationWords:
           direction = -direction
           continue
       if p in StopWord:
           continue
       if p == "but":
           direction = +1
           continue
       elif p in Nouns:
           Fptr.append( (p,i) )
           if p not in FeatureDict.keys():
               FeatureDict[p] = 0.0
               if p in WordsDict.keys():
                   FeatureDict[p] = WordsDict[p][0]*0.1
       elif p in WordsDict.keys():
            x = WordsDict[p][0]
            if x > 0.125 or x < -0.125:
                AdjPtr.append( (p,direction*WordsDict[p][0],i) )
     #print AdjPtr
     
#Pairing Adjectives and Nouns by computing distance.
#The adjective and noun with minimum distance between them will be paired.

     for i in range(len(AdjPtr)):
         dist = 1000000007
         feat = ""
         for j in range(len(Fptr)):
             if abs(AdjPtr[i][2] - Fptr[j][1]) < dist:
                 dist = abs(AdjPtr[i][2] - Fptr[j][1])
                 feat = Fptr[j][0]
         if feat != '':
             FeatureDict[feat] += AdjPtr[i][1]
         avg += AdjPtr[i][1]
         cnt += 1
         #test.append(AdjPtr[i][1])
         #print feat + " - " + AdjPtr[i][0] + " || " ,(AdjPtr[i][1]) 


 #print FeatureDict
 
# Computing the Score
 
 avg /= max(cnt,1)
  
# nscore = (x - minscore)/(maxscore - minscore)  
# handle rating part( thats left for computing the score) 
# If score > 2.5 , sentiment = Positive else sentiment = Negative
  
 normalizedscore = ((avg + 1)/2)*5

 # Taking 30% rating and 70% Score computed
 if rating >= 0:
     fscore = normalizedscore*0.7 + 0.3*rating
 else:
     fscore = normalizedscore*1.0
 
 print "Count: ", cnt
 #print "Size: ", len(test)
 print "Rating: ", rating
 print "Score: " ,avg
 print "Normalized Score: ", normalizedscore
 print "Final Score: ", fscore
 
 
 FinanceList = []
 LogisticsList = []
 QualityList = []
   
 LogisticsDept = ["slow", "behind", "belated", "blown", "delayed", "dilatory", "eleventh-hour", "gone", "jammed", "lagging", "overdue", "postponed", "remiss", "stayed", "tardy", "late", "unpunctual", "aboriginal", "antecedent", "antediluvian", "antiquated", "preceding", "premier", "prevenient", "primal", "prime", "primitive", "primordial", "prior", "pristine", "proleptical", "raw", "undeveloped", "gradual", "heavy", "lackadaisical", "leisurely", "lethargic", "moderate", "passive", "quiet", "reluctant", "sluggish", "stagnant", "crawling", "creeping", "dawdling", "delaying", "deliberate", "disinclined", "idle", "lagging", "loitering", "measured", "plodding", "postponing", "procrastinating", "slack", "apathetic", "dilatory", "dreamy", "drowsy", "imperceptible", "inactive", "indolent", "leaden", "negligent", "slow-moving", "snaillike", "torpid", "tortoiselike"]
   
 FinanceDept = ["costly", "extravagant", "high", "lavish", "overpriced", "pricey", "valuable", "excessive", "exorbitant", "immoderate", "inordinate", "invaluable", "posh", "rich", "swank", "uneconomical", "unreasonable", "economical", "reasonable", "worthless", "cheap", "inexpensive", "moderate", "agile", "nimble", "accelerated", "electric", "flashing", "flying", "snap", "winged", "breakneck", "highprice", "price", "priced", "cost"]
 
 QualityDept = ["complicated", "confusing", "flawed", "imprecise", "inaccurate", "incomplete", "incorrect", "useful", "not ", "pointless", "ugly", "unfinished", "unreliable", "useless", "appropriate", "attractive", "convenient", "faultless", "flawless", "free of error", "handy", "helpful ", "practical", "precise", "quality", "useful ", "acceptable", "bad", "excellent", "exceptional", "favorable", "great", "marvelous", "positive", "satisfactory", "satisfying", "superb", "valuable", "wonderful", "ace", "boss", "bully", "capital", "choice", "crack", "nice", "pleasing", "prime", "rad", "sound", "spanking", "sterling", "super", "superior", "welcome", "worthy", "admirable", "agreeable", "commendable", "congenial", "deluxe", "first-class", "first-rate", "gratifying", "honorable", "neat", "precious", "reputable", "select", "shipshape", "splendid", "stupendous", "poor", "dreadful", "atrocious", "cheap", "unacceptable", "sad", "lousy", "crummy", "awful", "rough", "synthetic", "gross", "imperfect", "bummer", "garbage", "blah", "diddly", "inferior", "downer", "abominable", "amiss", "bad news", "beastly", "careless", "cheesy", "crappy", "defective", "deficient", "satisfactory", "erroneous", "fallacious", "faulty", "grungy", "icky", "inadequate", "incorrect", "off", "raunchy", "slipshod", "stinking", "substandard", "unsatisfactory", "junky", "bottom out", "not good"]
 
# Initializing the Lists   
 FinanceList.append(0)
 LogisticsList.append(0)
 QualityList.append(0)
   
 a = rev
 v = a.split('.')
 #print "V " ,v
 S = 0   
 for sentence in v:
  S = S + 1
  z = sentence.split(' ')
  #print z,S
  for c in z:
     c = c.lower()
     if c in FinanceDept and S not in FinanceList:
        FinanceList.append(S)
     if c in LogisticsDept and S not in LogisticsList:
        LogisticsList.append(S)
     if c in QualityDept and S not in QualityList:
        QualityList.append(S)
        
 str1 = ','.join(str(e) for e in FinanceList) 
 str2 = ','.join(str(e) for e in QualityList)
 str3 = ','.join(str(e) for e in LogisticsList)
 
 print "str1: ",str1
 print "str2: ",str2
 print "str3: ",str3 
 
 ret = {}
 ret["rep_score"] = fscore
 ret["logisticsDept"] = str3
 ret["financeDept"] = str1
 ret["qualityDept"] = str2
 
 return ret

print "Exec"
rev = "\"english teachers work native speakers languages thrilled flash cards. handsomely printed durable stock protective coating years shuffling. making twenty years result approached artful clear design sturdy compact cards. students linguistics find cards developing fluency ipa transcription.the transcription example english nice compromise overly broad unnecessarily narrow. diacritics example limited markers length syllabicity. general american accent model primary secondary stress marked syllable boundaries. esolefl teachers 43 cards covering sounds american english conveniently colorcoded deck 2 distinguish rest. linguistics students spend time decks symbol side its phonetic description reverse names individual symbols. decision separate decks package three decks generous wise: higher price capability accurately describe languages students hail south sudanone complain tool teaching sounds language sounds audibly. folks minokidowinan app iphone works task flashcards best suited improving fluency phonetic transcription written exercise. \""
solve(rev,5)
  
