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
'''
I used these links as test cases. 
https://en.wikipedia.org/wiki/Special:Random worked fine as well

url =  "https://en.wikipedia.org/wiki/Science" 
url = "https://en.wikipedia.org/wiki/Natural_science"
url = "https://en.wikipedia.org/wiki/International_law"
url = "https://en.wikipedia.org/wiki/Politics"
url = "https://en.wikipedia.org/wiki/Tokyo"
'''

url = "https://en.wikipedia.org/wiki/Special:Random"
##################################
number_of_searches = 50
s = 0
while s < number_of_searches:
    def popTags(text):
        # parentheses
        text = re.sub(r'\(from .+\)|\(<a .+\)', '', str(text))
        # sup tags
        text = re.sub('<sup(.+?)/sup>', '',str(text))
        return(text.strip())
    
    def tillPhilosophy(url):
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #title = soup.find(id="firstHeading").text
        
        results = soup.find_all('div', {'class' : 'mw-parser-output'})
    
        paragraph = results[0].find_all('p')[0]
        
        # if paragraph <p></p> is empty, go to the next p
        while paragraph.find('a') is None:
            paragraph = paragraph.find_next_sibling('p')
            
        if paragraph.span is not None:
            paragraph.span.clear()    
        else:
            pass
        
        # get the text of paragraph
        p_text = paragraph.get_text
        
        # remove noise links from tables, foot/hat/notes etc. & recreate BS object
        new_par = BeautifulSoup(popTags(p_text))
        return('https://en.wikipedia.org' + new_par.find('a')['href'], soup.find(id="firstHeading").text)
    
    # =============================================================================
    #url = "https://en.wikipedia.org/wiki/Special:Random"
    
    next_link, title = tillPhilosophy("https://en.wikipedia.org/wiki/Fact")
    
    while title != 'Philosophy':
        next_link, title = tillPhilosophy(url)
        print(title)
        url = next_link
    
    s +=1