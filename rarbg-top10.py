import sys
import json
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup as bs

# rarbg API call configuration
URL = ("https://torrentapi.org/pubapi_v2.php?" +
       "mode=list&" +
       "category=52&" +
       "sort=leechers&" +
       "token=lnjzy73ucv&" +
       "format=json_extended&" +
       "app_id=tmlist")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
           'AppleWebKit/537.36 (KHTML, like Gecko) ' +
           'Chrome/92.0.4515.159 ' +
           'Safari/537.36'}

time.sleep(2)  # timeout required
rarbg = requests.get(URL, headers=headers)

if 'error' in rarbg.json() :
    print("Faild 1st try")
    time.sleep(5)  # timeout required
    rarbg = requests.get(URL, headers=headers)

    if 'error' in rarbg.json() :
        print("Faild 2nd try")
        time.sleep(5)  # timeout required
        rarbg = requests.get(URL, headers=headers)

        if 'error' in rarbg.json() :
            print("Faild 3rd try")
            sys.exit("API Fail")

rarbg_json = json.loads(rarbg.text)
rarbg_torrent_list = rarbg_json['torrent_results']

# create top 10 list with necessary data
rarbg_top10_list = [[None, None, None]] * 10

for i in range(len(rarbg_torrent_list)):
    if rarbg_top10_list[-1] != [None, None, None]:
        break
    else:
        for j in range(len(rarbg_top10_list)):
            if rarbg_top10_list[j][0] is None:
                rarbg_top10_list[j] = (rarbg_torrent_list[i]['episode_info']['imdb'],
                                       rarbg_torrent_list[i]['leechers'],
                                       rarbg_torrent_list[i]['seeders'])
                break
            else:
                if rarbg_top10_list[j][0] == rarbg_torrent_list[i]['episode_info']['imdb']:
                    break

# create movies list
movies = [{"Title": "", "Year": "", "Genre": "", "Plot": "", "Director": "",
           "Writer": "", "Actors": "", "Poster": "", "Metascore": "",
           "imdbRating": "", "imdbVotes": "", "imdb": "",
           "leechers": "", "seeders": ""}
          for i in range(len(rarbg_top10_list))]

# fill movies list with metadata from the open movie database
for i in range(len(rarbg_top10_list)):
    movie_db = requests.get("http://www.omdbapi.com/?apikey=4a43ddc9&i=" +
                            rarbg_top10_list[i][0],
                            headers=headers)

    movie_db_json = json.loads(movie_db.text)

    movies[i]['Title'] = movie_db_json['Title']
    movies[i]['Year'] = movie_db_json['Year']
    movies[i]['Genre'] = movie_db_json['Genre']
    movies[i]['Plot'] = movie_db_json['Plot']
    movies[i]['Director'] = movie_db_json['Director']
    movies[i]['Writer'] = movie_db_json['Writer']
    movies[i]['Actors'] = movie_db_json['Actors']
    movies[i]['Poster'] = movie_db_json['Poster']
    movies[i]['Metascore'] = movie_db_json['Metascore']
    movies[i]['imdbRating'] = movie_db_json['imdbRating']
    movies[i]['imdbVotes'] = movie_db_json['imdbVotes']
    movies[i]['imdb'] = rarbg_top10_list[i][0]
    movies[i]['leechers'] = rarbg_top10_list[i][1]
    movies[i]['seeders'] = rarbg_top10_list[i][2]

    time.sleep(1)

# convert the movies list to pandas dataframe
df = pd.DataFrame(movies,
                  index=[i for i in range(1, 11)],
                  columns=list(movies[0]))

# export dataframe to csv file
df.to_csv('data/movie_list.csv')
print(df["Title"].to_string())

# change the web page according to the updated movies list
html = open('./index.html')
soup = bs(html, "html.parser")

for i in range(len(rarbg_top10_list)):

    soup.find(id=i).a.attrs['href'] = "https://rarbgto.org/torrents.php?imdb=" + movies[i]['imdb']
    soup.find(id=i).a.img.attrs['src'] = movies[i]['Poster']
    soup.find(id=i).h3.string = movies[i]['Title'] + " (" + movie_db_json['Year'] + ")"
    soup.find(id=i).h4.string = movies[i]['Genre']
    soup.find(id=i).h6.string = "IMDB rating: " + movies[i]['imdbRating'] + "/" + movies[i]['imdbVotes']
    soup.find(id=i).p1.string = movies[i]['Plot']
    soup.find(id=i).p2.string = "Director: " + movies[i]['Director']
    soup.find(id=i).p3.string = "Wirter: " + movies[i]['Writer']
    soup.find(id=i).p4.string = "Actors: " + movies[i]['Actors']

html.close()
html_new = soup.prettify("utf-8")
with open("./index.html", "wb") as file:
    file.write(html_new)
