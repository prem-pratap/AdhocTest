#!usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import html5lib 
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from  nltk.corpus   import  stopwords
import string
from pyspark import SparkContext,SparkConf 
from  nltk.stem import WordNetLemmatizer
import os
url = "https://en.wikipedia.org/wiki/Machine_learning"

r  = requests.get(url)

soup=BeautifulSoup(r.content,'html5lib')
#opening files 
fp1=open('./Data_extracted.txt','w+')
fp2=open('./Lemmatized_data.txt','w+')
fp3=open('./Final_data.txt','w+')
data_content=[]
data_heading=[]
t1=soup.find('body',attrs={'class':'mediawiki ltr sitedir-ltr mw-hide-empty-elt ns-0 ns-subject mw-editable page-Machine_learning rootpage-Machine_learning skin-vector action-view'})
#t2=soup.find('div',attrs={'id':'layout'})
for row in t1.find_all('p'):
        d1=[]
        d1=row.text
        data_content.append(d1)

for row in t1.find_all('span',attrs={'class':'mw-headline'}):
        d2=[]
        d2=row.text
        data_heading.append(d2)
fp1.write(data_content[0]+'\n')
fp1.write(data_heading[0]+'\n')
fp1.write(data_content[1]+'\n')
fp1.write(data_heading[1]+'\n')
for i in range(3,7):
	fp1.write(data_content[i])
fp1.close()
#reading file for lemmatization 
inputfile=open('Data_extracted.txt','r')
#Lemmatizing input data of read file
lemma=WordNetLemmatizer()
for j in inputfile:
	tokens=word_tokenize(j)
	newword=[lemma.lemmatize(word) for word in tokens]
	fp2.write(' '.join(newword))
fp2.close()
#Again opening for removing stop words
fp2=open('Lemmatized_data.txt','r+')
for  j  in fp2:
	words=word_tokenize(j)
	alphadata=[word for word in words if word.isalpha()]
	newword1=[word for word  in  alphadata if word not in (stopwords.words('english') and string.punctuation) ]
	fp3.write(' '.join(newword1))
inputfile.close()
fp2.close()
fp3.close()

#count words
input_file=sc.textFile("./Final_data.txt")
words=input_file.flatMap(lambda line : line.split(" "))
count=words.map(lambda word :(word,1)).reduceByKey(lambda a,b:a+b)
all_words=[]
values=[]
for i in count.collect():
	all_words.append(i[0])
	values.append(i[1])
	
