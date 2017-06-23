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

It's actually super annoying to use, crashes about every ~300 entries on average.
1000 at best

!!!!If it crashes, the best advice I can give is to record
the last id printed and change the while loop in line 32 to start at that (id+1)

So these problems may or may not be fixed in the future - the purpose of this code is to generate 
a csv file which I can use for additional processing later anyways. 

The csv will be accurate as of May 29 2017

edit:kms i forgot # of people scored oh well <- I will add this in soon because I wanna use it
"""

#importing relevant libraries 
import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import time

#results are the variables I'm interested in, info are columns that share a similar 
#structure in the html
results = {"ID":[], "Title":[], "Type":[], "Episodes":[], "Status":[], "Aired":[], "Premiered":[], "Broadcast":[],
           "Producers":[], "Licensors":[], "Studios":[], "Source":[], "Genres":[], "Duration":[], "Rating":[],
           "Score":[], "Users Scored":[], "Ranked":[], "Popularity":[], "Members":[], "Favorites":[]}

info = ["Type", "Episodes", "Status", "Aired", "Premiered", "Broadcast", "Producers", "Licensors", "Studios", "Source", "Genres",
        "Duration", "Rating", "Score", "Ranked", "Popularity", "Members", "Favorites"]

nested_info = ["Type", "Premiered", "Producers", "Licensors", "Studios", "Genres", "Score"]

#MAL has a quite convenient characteristic that every page can be found using /anime/showid
#where id is a number from 1 to some large number I don't know
def get_mal_html():
    url = 'https://myanimelist.net/anime/'
    for attempt in range(10):
        try:
            r = requests.get(url + str(i), headers={'User-agent': 'your bot 0.1'})  # so we don't get flagged as a bot
            return r.text
        except:
            print("Resending get request")
            time.sleep(5)
            continue
    raise ValueError('HTML failed to be obtained')

#Takes a navigatable string from BeautifulSoup api and cleans it into a standard unicode string
def clean_nav_string(nav_string):
    unicode_string = str(nav_string.encode('utf-8'))[2:-1]
    unicode_string = unicode_string.replace("\\n", "")
    unicode_string = unicode_string.strip()
    return unicode_string

#Grabs and appends all string values together from all nested elements within the main_element
def get_value_from_nested_elements(main_element):
    value = ""
    for sibling in (main_element.next_siblings):
        if sibling.string != None:
            value = value + ' ' + clean_nav_string(sibling.string)
            value = value.strip()
    return value

#this should go from 1 to 100000 (some arbitrarily large number)
#however, I often change the range because the program crashes
#edit: new try/except statement should fix most of these problems
for i in range(0,6):
    try:
        mal_html = get_mal_html()
    except ValueError as err:
        print(err.args)
        print("Error on: ", i)
        break

    mal_soup = BeautifulSoup(mal_html)
    title = mal_soup.title.string[1:-19]

    print(i)
    print((str(title.encode('utf-8')))[2:-1])

    if "04 Not Found" in title: #some pages return 404's, filter them out
        continue

    results["ID"].append(i)
    results["Title"].append((str(title.encode('utf-8')))[2:-1])

    #Use BeautifulSoup to find locations of all relevant info - all of them are under "dark_text" spans
    data = mal_soup.find_all("span", class_="dark_text")
    for element in data:
        index = element.string[:-1]
        if (index in info):
            if (index in nested_info): #Relevant info lays deeper in nested elements
                value = get_value_from_nested_elements(element)
            else:
                value = element.next_sibling.string
                value = clean_nav_string(value)
            results[index].append(value)

    #Fill in missing/inapplicable data to maintain table consistency
    for i in results:
        if len(results[i]) != len(results["ID"]):
            results[i].append(-1)

#Parse Score data in numerical score value and number of users scored
for i in range(len(results["Score"])):
    results["Users Scored"][i] = results["Score"][i][18:-7]
    results["Score"][i] = results["Score"][i][0:4]

df = pd.DataFrame(results)
df2 = df.set_index("ID")
with open('mal_data.csv', 'a') as f:
    df2.to_csv(f, header=False)

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