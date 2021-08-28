[![Update Movie List](https://github.com/ErezWeiss1/Trending_Movies/actions/workflows/UpdateMovieList.yml/badge.svg)](https://github.com/ErezWeiss1/Trending_Movies/actions/workflows/UpdateMovieList.yml)

# Trending_Movies

The goal of this project is to create web page containing the top 10 trending 4K/x265/HDR movies from the public torrent tracker rarbg.to, automating the task of finding a good movie to watch at the end of the day.

The raw data is gathered using the API:

https://torrentapi.org/apidocs_v2.txt?app_id=lol

which provides a list of the 25 most leeched releases from the 4K/x265/HDR category.

The list is then trimmed down to the top 10 individual movie titles and keeping the imdb_ID, #leechers,#seeders and transfered to a new "Movies" list with metadata placeholders.

The metadata is gathered using the API:

http://www.omdbapi.com/

and injected into the "Movies" list which then converted to [pandas](https://github.com/pandas-dev/pandas) DataFrame 

 Outputs:
 
 *prints the DataFrame
 *export DataFrame to .csv file in the ./data folder
 *changes the .html file using [BeatifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

the script is scheduled to run once a day through github actions.<br>



Check out more projects by me here:

https://erezweiss1.github.io/

