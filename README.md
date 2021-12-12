[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Facebook automatic Room Listings fetch&filter

### Description
The goal of this code is as follows:

1. Scrape pre-determined Facebook groups for room listings in Amsterdam (currently, Zoekt Kamer in Amsterdam Community).

2. Filter the rooms on the criteria you set, eg. price, location, size of the room

3. Send the matches to your email, daily. 

### About the code
This project heavily relies on the already existing Facebook scraper found here : [Facebook-scraper](https://github.com/kevinzg/facebook-scraper).

In the repository also resides a CSV file from the city of Amsterdam, containing all the adresses of Amsterdam. (Freely accessible from https://data.amsterdam.nl ).

### usage
First, make sure you install the Facebook scraper from Kevin's repo (listed above).

In the repository file, you shoud insert a `cookies.json` file, containing your Facebook cookies, in JSON format. See Kevin's page for more info

Set your criteria : locations of interest, (the easiest is to insert a list of postcodes), max price you are willing to pay, minimum room size, and Scrape away.

(Send to email function not implemented yet)

You should also probably have git LFS installed, as the large CSV file makes use of LFS (https://git-lfs.github.com/).

### Disclaimer
This is a non-serious project and is in a very imperfect state. Feel free to clone, fork, create pull requests.
