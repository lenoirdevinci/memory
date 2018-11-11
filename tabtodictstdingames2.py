import sys
import io
import json
import textblob
from textblob import TextBlob
#from nltk.tag.stanford import NERTagger as ner
import nltk
import pandas as pd
def dicti():
# THIS IS A SENTIMENT SCORER using afinn scores
# python tabtodictstdingames.py sentimentdict.txt data.json
# cd F:/RSAVED/scripts/Script20122013
# db.abnamro.find({"text" : /pronostic/},{text:1},{'user.description':1}).limit(10).pretty()
# retrieve text and name :  db.abnamro.find({"text" : /predict/},{text:1,'user.name':1}).pretty()
# pick up the largest account
# db.abnamro.find({"text" : /[1-9]*-[1-9]/,'user.followers_count': {$gte:200000}},{text:1,'user.description':1,'user.followers_count':1}).pretty()
# retrieve score results :
# export to mongo
#cd Desktop/DE/scripts/pythonnotes02082015/mongodb/bin
# ./mongoexport --db twitter --collection abnamro --csv --fields text --out first400.csv
# 
##THIS WILL IMPORT THE DICTIONNARY
	afinnfile = open(sys.argv[1],"r")#"C:\Python27\Scripts\AFINN-111.txt")# open("AFINN-111.txt")
	scores = {} # initialize an empty dictionary
	for line in afinnfile:
	  term, score  = line.split("\t")  # The file is tab-delimited ("\t"), we split it between term and score
	  #SCORES={term:score}
	  scores[term] = int(score)  # Convert the score to an integer.
	#print scores.items() # Print every (term, score) pair in the dictionary
	#print scores['unstoppable']
	
### THIS PART WILL LOAD A NEW TEXT TO BE SENTIMENT RATED AND TRANSFORM 
	i=0
	filetoscore=sys.stdin
	
	a={}
	a=filetoscore 
	b={}
	c={}
	scoresline={}
	result={}
	finalresult=[]
	#print len(a)
	passed = 0
	for line in a: # we have defined a as a dict so line in a will refer to items in that dict
		sys.stdout.flush()
		i=i+1
		try:
			b=json.loads(line) # we enforce a json format on each line
		except:
			pass
			passed = passed + 1
		#scoresfile=b.keys()
		try:
			c[i]=b["user"]["name"] + ' ::: '+ b["user"]["location"] + ' ::: ' +  b["user"]["followers_count"] + ' ::: ' + b['text'] # b['source'] + b['text'] +   c is a dict b is a dict we pick up the value of the key text 
			#print b['text']
		except Exception,e:
			c[i]= "00000"
			continue
		finally: 
			pass
	
### THIS PART WILL SCORE THE NEW TEXT, USING THE SCORES DICT COMPUTED PREVIOUSLY
	#print c.items()
	for twit in c.values():
		linescore=0
		for word in twit.split():
			try:
				#print word , scores[word]
				scoresline= word,scores[word]
				linescore = linescore + scores[word]
			except Exception,e:
				scoresline= word,"Text not found"
		#print "linescore" + str(linescore)
		result[twit]= linescore, TextBlob(twit).sentiment.polarity #, nltk.ne_chunk(nltk.pos.tag(nltk.word_tokenize(twit.split())))
	
	try:
		for res in result.items():
			#if res[1][1] < -0.50 :  # this will look at the very positive feeling from manual tagging 
			#if res[1][1] * res[1][0] < -1 : # pick up cases when they disagree strongly
			if res[1][1] < -0.5 and res[1][0] < 0 :
				finalresult.append(res)
			print (res[0] ,res[1][0], res[1][1]),'\n'
			sys.stdout.flush()
	except:
		pass
	print i
	#q =open('SENTIMENTSRESULTS.TXT','w+')
	#q.write(str(result.items()) , '\n')
	#q.close()
	#pd.DataFrame(finalresult).to_csv('doubleSentiment.csv')
	
if __name__ == "__main__":
	dicti()
	
	
	

