#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 13:28:33 2018

@author: stephanosarampatzes
"""

import requests
from bs4 import BeautifulSoup
#import urllib.request
import re


url = "https://en.wikipedia.org/wiki/Special:Random"

#################

def popTags(text):
    # parentheses
    text = re.sub(r'\(from(.+?)\)|\(<.(.+?)\)', '', str(text))
    # sup tags
    text = re.sub('<sup(.+?)/sup>', '',str(text))
    # sup tags
    text = re.sub('<small(.+?)/small>', '',str(text))
    return(text.strip())
    
def tillPhilosophy(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
        
    #title = soup.find(id="firstHeading").text
        
    results = soup.find_all('div', {'class' : 'mw-parser-output'})
    
    paragraph = results[0].find_all('p')[0:2]
    
    # if paragraph <p></p> is empty, go to the next p
    if paragraph[0].find('a') is None :
        paragraph = paragraph[1]
        while paragraph.find('a') is None:
            paragraph = paragraph.find_next_sibling('p')
    else:
        paragraph = paragraph[0]
    
    # clear some span
    if paragraph.span is not None:
        paragraph.span.clear()    
    else:
        pass
        
    # get the text of paragraph
    p_text = paragraph.get_text
        
    # remove noise links from tables, foot/hat/notes etc. & recreate BS object
    new_par = BeautifulSoup(popTags(p_text),'lxml')
    return('https://en.wikipedia.org' + new_par.find('a')['href'], soup.find(id="firstHeading").text)
    
# =============================================================================
    
next_link, title = tillPhilosophy(url)

number_of_searches = 50
s = 0    
  
while title != 'Philosophy' and s < number_of_searches:
    print(title)
    next_link, title = tillPhilosophy(url)
    url = next_link
    
    s +=1
    if s == number_of_searches:
        print('\n','Infinite Loop ∞')
        