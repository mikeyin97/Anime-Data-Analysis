"""
MAL DATA SCRAPER
MAL has a wealth of interesting information on every anime page.
I wanted to use this information in order to find patterns, visualize trends, etc. 
However, in order to do that, I needed to retrieve the data in a usable format. 

MAL has a pretty underdeveloped API that lacks a lot of query options. As a result, 
I developed this data scraper that basically reads html from each anime page and
retrieves the important information. 

The code is pretty hacked together and occasionally crashes - sometimes due to my
coding incompetencies and sometimes due to MAL servers. It also doesn't read
special unicode characters. Also MAL webpages for some reason decided to change html
formatting somewhere in the 20000s so there are a lot of try/exceptions to account for 
that. 

So these problems may or may not be fixed in the future - the purpose of this code is to generate 
a csv file which I can use for additional processing later anyways. 

The csv will be accurate as of June 29 2017
"""

#importing relevant libraries 
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import time

#results are the variables I'm interested in, info are columns that share a similar 
#structure in the html
results = {"ID":[], "Title":[], "Type":[], "Episodes":[], "Status":[], "Aired":[], "Studios":[], "Source":[], "Genres":[], "Duration":[], "Rating":[], "Ranked":[], "Popularity":[], "Score":[], "ScoredBy":[]}
info = ["Type", "Episodes", "Status", "Aired", "Studios", "Source", "Genres", "Duration", "Rating", "Ranked", "Popularity"]

#MAL has a quite convenient characteristic that every page can be found using /anime/showid
#where id is a number from 1 to some large number I don't know
url = 'https://myanimelist.net/anime/'

#this should go from 1 to 100000 (some arbitrarily large number)
#however, I often change the range because the program crashes
#edit: new try/except statement should fix most of these problems

for i in range(35795,40000):
    r = requests.get(url + str(i),headers = {'User-agent': 'your bot 0.1'}) #so we don't get flagged as a bot
    data = r.text
    j=0
    while j<100:    #this while loop is here just to catch errors
        try:
            title_start = data.index('<title>')
            title_end = data.index('</title>')
            j = 100
        except:
            j+=1
            time.sleep(5)
            r = requests.get(url + str(i),headers = {'User-agent': 'your bot 0.1'}) #so we don't get flagged as a bot
            data = r.text
            pass
    title = (data[title_start+8:title_end-19])
    print(i)
    print((str(title.encode('utf-8')))[2:-1])
    if "404 Not Found" not in data: #some pages return 404's, filter them out
        results["ID"].append(i)
        results["Title"].append((str(title.encode('utf-8')))[2:-1])
        for k in info:
            j=0
            while j<100: 
                try:
                    info_text = '<span class="dark_text">' + k + ':</span>'
                    info_start = (data.index(info_text))
                    remaining = data[info_start: info_start + 1500]
                    info_end = (remaining.index('/div'))
                    j=100
                except:
                    j+=1
                    time.sleep(5)
                    pass
            if k == "Premiered":
                results[k].append((BeautifulSoup(remaining[3+len(info_text):info_end-16])).get_text())
            elif k == "Broadcast":
                results[k].append((BeautifulSoup(remaining[3+len(info_text):info_end-8])).get_text())
            elif k == "Ranked":
                results[k].append((BeautifulSoup(remaining[4+len(info_text):info_end-215])).get_text())
            elif k == "Popularity":
                results[k].append((BeautifulSoup(remaining[4+len(info_text):info_end-2])).get_text())
            else:
                results[k].append((BeautifulSoup(remaining[3+len(info_text):info_end-4])).get_text())
        try:
            score_text = '<span itemprop="ratingValue">'
            score_start = data.index(score_text)
            score = float(data[score_start+29:score_start+33])
            results["Score"].append(score)
            scoredby_text = '(scored by <span itemprop="ratingCount">'
            scoredby_start = data.index(scoredby_text)
            scoredby_text2 = '</span> users)'
            scoredby_end = data.index(scoredby_text2)
            scoredby = data[scoredby_start+40:scoredby_end]
            print(scoredby)
            scoredby = int(scoredby.replace(',', ''))
            results["ScoredBy"].append(scoredby)
        except:
            try:
                score_text = '<span class="dark_text">Score:</span>' #some of the scores are formatted differently
                score_start = data.index(score_text)
                score = (data[score_start+46:score_start+50])            
                results["Score"].append(score)
                if i == 31942:
                    results["ScoredBy"].append(17)
                else:
                    scoredby_text = '(scored by <span itemprop="ratingCount">'
                    scoredby_start = data.index(scoredby_text)
                    scoredby_text2 = '</span> users)'
                    scoredby_end = data.index(scoredby_text2)
                    scoredby = data[scoredby_start+40:scoredby_end]
                    print(scoredby)
                    scoredby = int(scoredby.replace(',', ''))
                    results["ScoredBy"].append(scoredby)
            except:
                score_text = 'Score:</span>'
                score_start = data.index(score_text)
                score = data[score_start+22:score_start+26]
                results["Score"][0]=(score)
                    
                scoredby_text = '(scored by <span>'
                scoredby_start = data.index(scoredby_text)
                scoredby_text2 = '</span> users)'
                scoredby_end = data.index(scoredby_text2)
                scoredby = data[scoredby_start+17:scoredby_end]
                scoredby = int(scoredby.replace(',', ''))
                print(scoredby)
                results["ScoredBy"].append(scoredby)
        #this probably wasn't very efficient but I set each row as a dataframe and append to the 
        #existing csv before resetting for the next id
        df = pd.DataFrame(results)
        df2 = df.set_index("ID")
        with open('my_csv2.csv', 'a') as f:
            df2.to_csv(f, header=False)
        results = {"ID":[], "Title":[], "Type":[], "Episodes":[], "Status":[], "Aired":[], "Studios":[], "Source":[], "Genres":[], "Duration":[], "Rating":[], "Ranked":[], "Popularity":[], "Score":[], "ScoredBy":[]}

    


