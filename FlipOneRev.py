#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 12 18:27:07 2021

@author: senthil
"""

import requests   
from bs4 import BeautifulSoup as bs 
import re 
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

macbook_reviews=[]
for i in range(1,30):
  mac=[]  
  url="https://www.flipkart.com/apple-macbook-air-core-i5-5th-gen-8-gb-128-gb-ssd-mac-os-sierra-mqd32hn-a-a1466/product-reviews/itmevcpqqhf6azn3?pid=COMEVCPQBXBDFJ8C&page="+str(i)
  response = requests.get(url)
  soup = bs(response.content,"html.parser")# creating soup object to iterate over the extracted content 
  reviews = soup.findAll("div",attrs={"class","t-ZTKy"})# Extracting the content under specific tags  
  stars=soup.findAll("div",attrs={"class","_3LWZlK _1BLPMq"})
  title=soup.findAll("p",attrs={"class","_2-N8zT"})
  for i in range(len(reviews)):
    mac.append(reviews[i].text)  
  macbook_reviews=macbook_reviews+mac 

#here we saving the extracted data 
print(type(macbook_reviews))


    
#mac_rev_string = " ".join(macbook_reviews) 

index=0
for name in macbook_reviews:
    print(index+1,macbook_reviews[index], end='\n')
    #print()
    index += 1
    
print(stars[0].text)
print(title[0].text)

with open("macbook.txt","w",encoding='utf8') as output:
    output.write(stars[0].text)
    output.write(title[0].text)
    output.write(str(macbook_reviews))