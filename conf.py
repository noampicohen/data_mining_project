#URL
URLS_NAME = ['ALL','ACTION','ANIMATION','ART_FOREIGN','CLASSIC','COMEDY','DOCUMENTARY','DRAMA','HORROR','FAMILY','MISTERY','ROMANCE','SCIFI']
URL_ALL = "https://www.rottentomatoes.com/browse/cf-dvd-streaming-all"
URL_ACTION = "https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=1&sortBy=release"
URL_ANIMATION = "https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=2&sortBy=release"
URL_ART_FOREIGN = "https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=4&sortBy=release"
URL_CLASSIC = "https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=5&sortBy=release"
URL_COMEDY = "https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=6&sortBy=release"
URL_DOCUMENTARY = "https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=8&sortBy=release"
URL_DRAMA = "https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=9&sortBy=release"
URL_HORROR = "https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=10&sortBy=release"
URL_FAMILY = "https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=11&sortBy=release"
URL_MISTERY = "https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=13&sortBy=release"
URL_ROMANCE = "https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=18&sortBy=release"
URL_SCIFI = "https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=14&sortBy=release"
ROTTEN_TOMATO_URL = "https://www.rottentomatoes.com"

#INPUT
INPUT_QUESTION = "path to chrome driver please:"

#HTML
BUTTON_ID = '//*[@id="show-more-btn"]/button'
HTML_PARSER = "html.parser"
HTML_ACTOR = 'cast-item media inlineBlock'
HTML_ACTOR_HIDE = 'cast-item media inlineBlock moreCasts hide'

#NUMERIC CONSTANT
SLEEP_TIME = 2
ZERO=0
ONE=1

# Constants from transform_box_office_to_number
MULTIPLE_DOLLARS = -1
BOX_OFFICE_FIRST = 1
BOX_OFFICE_LAST = -1
CONVERT_THOUSAND = 1000
CONVERT_MILLIONS = 1000000


# Constants from find_info
TOMATO_INDEX = 1
AUDIENCE_INDEX = 6
ELEMENT_ONE = 1

# Constants implement_movie
MAX_LENGTH_SYNOPSIS = 128
MAX_LENGTH_DATE = 12

#Constants for multiple functions
FIRST_ELEMENT = 0
COUNT_ZERO = 0

#Constants for arguments (main)
NUMBER_OF_ARGUMENTS = 4
FIRST_ARGUMENT = 1
CATEGORY = 0
NUMBER_OF_MOVIES = 1
SQL_PASSWORD = 2
CHROME_PATH_DRIVER = 3
