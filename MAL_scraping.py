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
special unicode characters. 

It's actually super annoying to use, crashes about every ~300 entries on average

!!!!If it crashes, the best advice I can give is to record
the last id printed and change the while loop in line 32 to start at that (id+1)

So these problems may or may not be fixed in the future - the purpose of this code is to generate 
a csv file which I can use for additional processing later anyways. 

The csv will be accurate as of May 29 2017

edit:kms i forgot # of people scored oh well
"""

#importing relevant libraries 
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import time

#results are the variables I'm interested in, info are columns that share a similar 
#structure in the html
results = {"ID":[], "Title":[], "Type":[], "Episodes":[], "Status":[], "Aired":[], "Studios":[], "Source":[], "Genres":[], "Duration":[], "Rating":[], "Ranked":[], "Popularity":[], "Score":[]}
info = ["Type", "Episodes", "Status", "Aired", "Studios", "Source", "Genres", "Duration", "Rating", "Ranked", "Popularity"]

#MAL has a quite convenient characteristic that every page can be found using /anime/showid
#where id is a number from 1 to some large number I don't know
url = 'https://myanimelist.net/anime/'

#this should go from 1 to 100000 (some arbitrarily large number)
#however, I often change the range because the program crashes
for i in range(3360,100000):
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
            pass
    title = (data[title_start+8:title_end-19])
    print(i)
    print((str(title.encode('utf-8')))[2:-1])
    if "404 Not Found" not in data: #some pages return 404's, filter them out
        results["ID"].append(i)
        results["Title"].append((str(title.encode('utf-8')))[2:-1])
        for i in info:
            j=0
            while j<100: 
                try:
                    info_text = '<span class="dark_text">' + i + ':</span>'
                    info_start = (data.index(info_text))
                    remaining = data[info_start: info_start + 1500]
                    info_end = (remaining.index('/div'))
                    j=100
                except:
                    j+=1
                    time.sleep(5)
                    pass
            if i == "Premiered":
                results[i].append((BeautifulSoup(remaining[3+len(info_text):info_end-16])).get_text())
            elif i == "Broadcast":
                results[i].append((BeautifulSoup(remaining[3+len(info_text):info_end-8])).get_text())
            elif i == "Ranked":
                results[i].append((BeautifulSoup(remaining[4+len(info_text):info_end-215])).get_text())
                #print([int(s) for s in k.split() if s.isdigit()])
            elif i == "Popularity":
                results[i].append((BeautifulSoup(remaining[4+len(info_text):info_end-2])).get_text())
            else:
                results[i].append((BeautifulSoup(remaining[3+len(info_text):info_end-4])).get_text())
        try:
            score_text = '<span itemprop="ratingValue">'
            score_start = data.index(score_text)
            score = float(data[score_start+29:score_start+33])
            results["Score"].append(score)
        except:
            score_text = '<span class="dark_text">Score:</span>' #some of the scores are formatted differently
            score_start = data.index(score_text)
            score = (data[score_start+46:score_start+50])
            
            
            results["Score"].append(score)
        #this probably wasn't very efficient but I set each row as a dataframe and append to the 
        #existing csv before resetting for the next id
        df = pd.DataFrame(results)
        df2 = df.set_index("ID")
        with open('my_csv.csv', 'a') as f:
            df2.to_csv(f, header=False)
        results = {"ID":[], "Title":[], "Type":[], "Episodes":[], "Status":[], "Aired":[], "Studios":[], "Source":[], "Genres":[], "Duration":[], "Rating":[], "Ranked":[], "Popularity":[], "Score":[]}

    #time.sleep(1)

"""

#bebop testing
url = 'https://myanimelist.net/anime/'
r = requests.get(url + str(1))
data = r.text
soup = BeautifulSoup(data, "lxml")
print(data)

for i in info:
    info_text = '<span class="dark_text">' + i + ':</span>'
    info_start = (data.index(info_text))
    remaining = data[info_start: info_start + 1500]
    info_end = (remaining.index('/div'))
    print (i + ":")
    if i == "Premiered":
        print((BeautifulSoup(remaining[3+len(info_text):info_end-16])).get_text())
    elif i == "Broadcast":
        print((BeautifulSoup(remaining[3+len(info_text):info_end-8])).get_text())
    elif i == "Ranked":
        k = ((BeautifulSoup(remaining[4+len(info_text):info_end-215])).get_text())
        print(k)
        #print([int(s) for s in k.split() if s.isdigit()])
    elif i == "Popularity":
        print((BeautifulSoup(remaining[4+len(info_text):info_end-2])).get_text())
    else:
        print((BeautifulSoup(remaining[3+len(info_text):info_end-4])).get_text())

score_text = '<span itemprop="ratingValue">'
score_start = data.index(score_text)
score = data[score_start+29:score_start+33]
print(score)
        
   



#print(data.index("<h2>Alternative Titles</h2>"))

"""