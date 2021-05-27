import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
import re

search_query="samsung+mobile+phone"
base_url="https://www.amazon.com/s?k="
url=base_url+search_query
header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36','referer':'https://www.amazon.com/s?k=nike+shoes+men&crid=28WRS5SFLWWZ6&sprefix=nike%2Caps%2C357&ref=nb_sb_ss_organic-diversity_2_4'}

search_response=requests.get(url,headers=header)
#print(search_response.status_code)
#print(search_response.text)
#print(search_response.cookies)

cookie={} # insert request cookies within{}
def getAmazonSearch(search_query):
    url="https://www.amazon.com/s?k="+search_query
    page=requests.get(url,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"
    
def Searchasin(asin):
    url="https://www.amazon.com/dp/"+asin
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"
    
def Searchreviews(review_link):
    url="https://www.amazon.com"+review_link
    page=requests.get(url,cookies=cookie,headers=header)
    if page.status_code==200:
        return page
    else:
        return "Error"

product_names=[]
response=getAmazonSearch('samsung+mobile+phone')
soup=BeautifulSoup(response.content,features="lxml")
for i in soup.findAll("span",{'class':'a-size-medium a-color-base a-text-normal'}): # the tag which is common for all the names of products
    product_names.append(i.text) #adding the product names to the list

#print(product_names)

data_asin=[]
response=getAmazonSearch('samsung+mobile+phone')
soup=BeautifulSoup(response.content,features="lxml")
for i in soup.findAll("div",{'class':"s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 AdHolder sg-col sg-col-12-of-16"}):
    data_asin.append(i['data-asin'])
    
#print(response.status_code)
#print(data_asin)
#print(len(data_asin))

link=[]
for i in range(1):
    response=Searchasin(data_asin[i])
    soup=BeautifulSoup(response.content,features="lxml")
    for i in soup.findAll("a",{'data-hook':"see-all-reviews-link-foot"}):
        link.append(i['href'])

reviews=[]
for j in range(1):
    for k in range(10):
        response=Searchreviews(link[j]+'&pageNumber='+str(k))
        soup=BeautifulSoup(response.content,features="lxml")
        for i in soup.findAll("span",{'data-hook':"review-body"}):
            reviews.append(i.text)

rev={'reviews':reviews}

review_data=pd.DataFrame.from_dict(rev)
pd.set_option('max_colwidth',800)

#print(product_names[0])
#print(type(review_data))
#print(reviews)

str1=" "
for ele in reviews: 
    str1 += ele 
    
sentence_list = nltk.sent_tokenize(str1)

val=1
for sen in sentence_list:
    #print(val,sen)
    val=val+1

formatted_article_text = re.sub('[^a-zA-Z]', ' ', str1 )
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

maximum_frequncy = max(word_frequencies.values())
print(maximum_frequncy)
#print(word_frequencies.values(),word_frequencies.items())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
    
sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 20:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]
                    
import heapq
summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)
#print(type(summary))
    
sen_list = nltk.sent_tokenize(summary)

val=1
for sen in sen_list:
    print(val,sen)
    val=val+1