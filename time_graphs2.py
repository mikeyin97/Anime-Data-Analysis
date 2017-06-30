import seaborn as sns
import pandas as pd
import inspect
import os
import matplotlib.pyplot as plt
import numpy as np

def initialize_data():
    sns.set()
    #sns.set_style("whitegrid")
    tips = sns.load_dataset("tips")
    
    module_path = inspect.getfile(inspect.currentframe())
    module_dir = os.path.realpath(os.path.dirname(module_path))
    
    data = pd.read_csv(module_dir+"/mal_data.csv", encoding = "ISO-8859-1")
    data = data.set_index("ID")
    print(list(data.columns.values))
    
    data[['Score','Popularity']] = data[['Score','Popularity']].apply(pd.to_numeric,errors='coerce')
    tv_data = data[data["Type"] == "TV"]
    ova_data = data[data["Type"] == "OVA"]
    combined_data = pd.concat([tv_data, ova_data])
    non_h_combined_data = combined_data[combined_data["Rating"] != "Rx - Hentai"]
    return non_h_combined_data
    
    #gotta take out the data with less thna 50 users

#how have genres changed over the years
#how has scoring changed over the years 
#how has source changed over the years 

#remind me to filter out things under a threshold of viewed users - skews rating p hard

#genre/score/popularity for each studio (box plot chart for genres, diff graph per studio)

#histograms? beanplots?

# get top 100? 500? list and look at genres

def ecdf(data):
    """Compute ECDF for a one-dimensional array of measurements."""

    # Number of data points: n
    n = len(data)

    # x-data for the ECDF: x
    x = np.sort(data)

    # y-data for the ECDF: y
    y = np.arange(1, n+1) / n

    return x, y

def studio_vs_ratings(non_h_combined_data):
    
    all_studio_data = []
    studio_means = []
    studio_stddev = []
    
    x = []
    y = []
    
    non_h_combined_data['Std'] = ""
    for studio in (non_h_combined_data.Studios.unique()):
        if ("," not in studio) and (studio != "None found, add some") and ((non_h_combined_data['Studios'] == studio).sum() > 20):
            studio_data = non_h_combined_data[non_h_combined_data['Studios'].str.contains(studio)]
            (studio_data.loc[:,['Std']]) = studio 
            all_studio_data.append(studio_data)
            studio_means.append(round(float(studio_data.loc[:,["Score"]].mean()),2))
            studio_stddev.append(round(float(studio_data.loc[:,["Score"]].std()),2))
            
            a,b = ecdf(studio_data["Score"].tolist())
            x.append(a)
            y.append(b)
            print(type(x))
    result = pd.concat(all_studio_data)
    print(studio_means)
    print(studio_stddev)
    for i in range(len(x)):
        plt.plot(x[i], y[i], marker = ".", linestyle = "none")
    #ax = sns.boxplot(x="Std", y="Score", data=result)
    #plt.xticks(rotation=90)
    #plt.tight_layout()
    sns.plt.show()
    
def studio_vs_popularity(non_h_combined_data):
    
    all_studio_data = []
    non_h_combined_data['Std'] = ""
    for studio in (non_h_combined_data.Studios.unique()):
        if ("," not in studio) and (studio != "None found, add some") and ((non_h_combined_data['Studios'] == studio).sum() > 20):
            studio_data = non_h_combined_data[non_h_combined_data['Studios'].str.contains(studio)]
            (studio_data.loc[:,['Std']]) = studio 
            all_studio_data.append(studio_data)
        
    result = pd.concat(all_studio_data)

    ax = sns.boxplot(x="Std", y="Popularity", data=result)
    plt.xticks(rotation=90)
    plt.tight_layout()
    sns.plt.show()

def source_vs_ratings(non_h_combined_data):
    
    all_source_data = []
    source_means = []
    source_stddev = []
    
    for source in (non_h_combined_data.Source.unique()):
        source_data = non_h_combined_data[non_h_combined_data['Source'] == source] 
        all_source_data.append(source_data)
        source_means.append(round(float(source_data.loc[:,["Score"]].mean()),2))
        source_stddev.append(round(float(source_data.loc[:,["Score"]].std()),2))
    result = pd.concat(all_source_data)
    
    ax = sns.boxplot(x="Source", y="Score", data=result)
    print(source_means)
    print(source_stddev)
    plt.xticks(rotation=45)
    plt.tight_layout()
    sns.plt.show()
    
def source_vs_popularity(non_h_combined_data):
    
    all_source_data = []
    source_means = []
    source_stddev = []
    
    for source in (non_h_combined_data.Source.unique()):
        source_data = non_h_combined_data[non_h_combined_data['Source'] == source] 
        all_source_data.append(source_data)
        source_means.append(round(float(source_data.loc[:,["Popularity"]].mean()),2))
        source_stddev.append(round(float(source_data.loc[:,["Popularity"]].std()),2))
    result = pd.concat(all_source_data)
    
    ax = sns.boxplot(x="Source", y="Popularity", data=result)
    print(source_means)
    print(source_stddev)
    plt.xticks(rotation=45)
    plt.tight_layout()
    sns.plt.show()

def genre_vs_ratings(non_h_combined_data):
    temp = non_h_combined_data
    non_h_combined_data = non_h_combined_data.astype('object')
    for i in non_h_combined_data.index.values.tolist():
        a = [x.strip() for x in non_h_combined_data.loc[i]["Genres"].split(',')]
        non_h_combined_data["Genres"][i] = a
    
    unique_genres = []
    count = 0
    for genre_list in non_h_combined_data["Genres"]:
        for j in range(len(genre_list)):
                if genre_list[j] not in unique_genres:
                        unique_genres.append(genre_list[j])
        
        count += 1

    unique_genres.remove('No genres have been added y')
    print(unique_genres)
    
    non_h_combined_data = temp
    non_h_combined_data['Genre'] = ""
    all_genre_data = []
    for genre in (unique_genres):
        genre_data = non_h_combined_data[non_h_combined_data['Genres'].str.contains(genre)]
        (non_h_combined_data.head())
        genre_data.loc[:,['Genre']] = genre
        all_genre_data.append(genre_data)
    result = pd.concat(all_genre_data)
    
    ax = sns.boxplot(x="Genre", y="Score", data=result)
    plt.xticks(rotation=90)
    plt.tight_layout()
    sns.plt.show()
    

def testing(non_h_combined_data):
    #print((non_h_combined_data.Source.value_counts()))
    #print (non_h_combined_data.index)
    return
    
if __name__ == "__main__":
    data = initialize_data()
    studio_vs_ratings(data)
    testing(data)
    