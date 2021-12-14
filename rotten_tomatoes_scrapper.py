import conf
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import sys
import pymysql
from datetime import datetime
import requests
import json
import ERD



def transform_box_office_to_number(box_office):
    """

    :param box_office: string with letters
    :return: an int according to the value of the string
    """
    if box_office[conf.MULTIPLE_DOLLARS] == 'K':
        return round(float(box_office[conf.BOX_OFFICE_FIRST: conf.BOX_OFFICE_LAST])) * conf.CONVERT_THOUSAND
    if box_office[conf.MULTIPLE_DOLLARS] == 'M':
        return round(float(box_office[conf.BOX_OFFICE_FIRST: conf.BOX_OFFICE_LAST])) * conf.CONVERT_MILLIONS
    else:
        return None


def check_exists_by_xpath(driver, xpath):
    """
    check if we can load more movies in the main page
    :param xpath: path to xpath of the button "show more"
    :return: true if the button exist , else false
    """
    try:
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True


def scrap_main_page(url, chrome_path):
    """

    :param url: url given by the user
    :return: a list of dict containing name , release date , and link to the website of the movie
    """
    movies = []
    driver = webdriver.Chrome(chrome_path)
    driver.get(url)
    click_more = driver.find_element(By.XPATH, conf.BUTTON_ID)
    # load all the main pages until the end
    while check_exists_by_xpath(driver, conf.BUTTON_ID):
        click_more.click()
        time.sleep(conf.SLEEP_TIME)

    content = driver.page_source
    soup = BeautifulSoup(content, features=conf.HTML_PARSER)
    count = conf.ZERO

    # find all the atributes needed from the main page and put it in a list of dict
    for element in soup.findAll('div', attrs={'class': 'movie_info'}):
        count += conf.ONE
        dic = {}
        title = element.find('h3', attrs={'class': 'movieTitle'})
        # release_date = element.find('p', attrs={'class': 'release-date'})
        url_page = element.find("a")['href']
        dic["movies"] = title.text
        # dic["release_date"] = release_date.text
        dic["url_page"] = conf.ROTTEN_TOMATO_URL + url_page
        movies.append(dic)
    driver.quit()
    return movies


def scrap_each_movie(movies, size_movies, chrome_path):
    """

    :param movies: list of dict containing name and url of movies
    :return: list of dict  with all info needed added
    """

    for i in range(size_movies):
        url_movie = movies[i]["url_page"]
        name_movie = movies[i]["movies"]
        try:
            info_movie = find_info(url_movie, name_movie, chrome_path)
            movies[i].update(info_movie)
        except Exception:
            pass
    return movies


def find_info(url_movie, name_movie, chrome_path):
    """

    :param url_movie: receive url of a movie
    :return: list with all info needed and found on the movie
    """
    actor_list = []
    driver = webdriver.Chrome(chrome_path)
    driver.get(url_movie)
    content = driver.page_source
    soup = BeautifulSoup(content, features=conf.HTML_PARSER)
    try:
        synopsis = ' '.join(soup.find(id='movieSynopsis').text.split())
        info_movie = {}
        info_movie['synopsis'] = synopsis
        for element in soup.find('ul', attrs={'class': 'content-meta info'}).findAll(class_='meta-row clearfix'):
            key = ' '.join(element.find(class_='meta-label subtle').text.split())[:-1]
            value = ' '.join(element.find(class_='meta-value').text.split())
            info_movie[key] = value
        rates = str(soup.find(id='topSection').find('score-board')).split()
        tomato_rate = rates[conf.TOMATO_INDEX].split('=')[conf.ELEMENT_ONE].replace("\"", "")
        audience_rate = rates[conf.AUDIENCE_INDEX].split('=')[conf.ELEMENT_ONE].replace("\"", "")
        info_movie['tomato_rate'] = tomato_rate
        info_movie['audience_rate'] = audience_rate

        actor_dict = []
        info_actors(soup, actor_dict, conf.HTML_ACTOR, actor_list)
        info_actors(soup, actor_dict, conf.HTML_ACTOR_HIDE, actor_list)

        info_movie['actors'] = ', '.join(actor_list)
        info_movie['youtube_trailer'] = trailer_url(name_movie)
        return info_movie
    except Exception:
        pass


def info_actors(soup, actor_dict, path, actor_list):
    """

    :return: in a specific page put in a list a dic withthe name of the actors ,
    their role and a url who lead to the actor page
    """

    for element in soup.findAll(class_=path):
        dict = {}
        try:
            url_page = element.find("a")['href']
            dict['url'] = conf.ROTTEN_TOMATO_URL + url_page
        except Exception:
            continue
        temp = element.text.splitlines()
        result = []
        [result.append(x.strip()) for x in temp if x.strip() != ""]
        name = result[conf.ZERO]
        dict['name'] = name.replace("'", "`")
        if len(result) > conf.ONE:
            role = result[conf.ONE]
            dict['role'] = role
        actor_list.append(dict['name'])
        actor_dict.append(dict)


def connect_to_database(password):
    """
    connect to your sql
    :param password: sql user password
    """
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=password)
    cursor = connection.cursor()
    return cursor, connection


def implement_movie(movie, cursor, name_movie):
    """
     insert all the movie indo into the sql tables movies
    :param movie: dic with movie info
    :param cursor: sql cursor
    :param name_movie: string mame of the movie
    :return: id_movie
    """
    id_language = None
    id_synopsis = None
    if 'Original Language' in movie.keys():
        language_movie = movie['Original Language']
    else:
        language_movie = None

    if 'synopsis' in movie.keys():
        if len(movie['synopsis']) >= conf.MAX_LENGTH_SYNOPSIS:
            text_synopsis = movie['synopsis'][:conf.MAX_LENGTH_SYNOPSIS].replace("'", "`")
        elif len(movie['synopsis']) > conf.ZERO:
            text_synopsis = movie['synopsis'].replace("'", "`")
        else:
            text_synopsis = None
    else:
        text_synopsis = None

    if 'url_page' in movie.keys():
        url_page = movie['url_page']
    else:
        url_page = None
    if 'Release Date (Streaming)' in movie.keys():
        date_streaming = datetime.strptime(movie['Release Date (Streaming)'][:conf.MAX_LENGTH_DATE].rstrip(),
                                           '%b %d, %Y').strftime(
            '%Y-%m-%d')
    else:
        date_streaming = None
    if 'Release Date (Theaters)' in movie.keys():
        date_theaters = datetime.strptime(movie['Release Date (Theaters)'][:conf.MAX_LENGTH_DATE].rstrip(),
                                          '%b %d, %Y').strftime(
            '%Y-%m-%d')
    else:
        date_theaters = None
    if 'tomato_rate' in movie.keys():
        tomato_rate = movie['tomato_rate']
    else:
        tomato_rate = None
    if 'audience_rate' in movie.keys():
        audience_rate = movie['audience_rate']
    else:
        audience_rate = None
    if 'Box Office (Gross USA)' in movie.keys():
        box_office = transform_box_office_to_number(movie['Box Office (Gross USA)'])
    else:
        box_office = None
    if 'youtube_trailer' in movie.keys():
        url_youtube_trailer = movie['youtube_trailer']
    else:
        url_youtube_trailer = None

    if language_movie is not None:
        cursor.execute(f"select count(name_language) from languages where name_language = ('%s')" % language_movie)
        checkcount_language = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]
        if checkcount_language == conf.COUNT_ZERO:
            cursor.execute(f'INSERT INTO languages (name_language) VALUES (%s)', language_movie)
        cursor.execute(f"select id_language from languages where name_language = ('%s')" % language_movie)
        id_language = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]
    if text_synopsis is not None:
        cursor.execute(f"select count(text_synopsis) from synopsis where text_synopsis = ('%s')" % text_synopsis)
        checkcount_synopsis = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]
        if checkcount_synopsis == conf.COUNT_ZERO:
            cursor.execute(f'''INSERT INTO synopsis (text_synopsis) VALUES (%s)''', text_synopsis)
        cursor.execute(f"""select id_synopsis from synopsis where text_synopsis = ('%s')""" % text_synopsis)
        id_synopsis = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]
    cursor.execute(
        f'INSERT INTO movies (name_movie,url_page,release_date_streaming ,release_date_theater ,rate_tomato,rate_audience ,boxoffice,languages_id_language,synopsis_id_synopsis,url_youtube_trailer) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        (name_movie, url_page, date_streaming, date_theaters, tomato_rate, audience_rate, box_office, id_language,
         id_synopsis, url_youtube_trailer))
    cursor.execute(f"select id_movies from movies where name_movie = ('%s')" % name_movie)
    id_movie = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]
    return id_movie


def implement_genre(movie, cursor, id_movie):
    """
    insert all the genre indo into the sql tables genre
    :param movie: dic with movie info
    :param cursor: sql cursor
    :return: id_movie
    """

    if 'Genre' in movie.keys():
        genres_movie = movie['Genre'].replace("'", "`").split(',')
        genres_movie = [genre.strip() for genre in genres_movie]
    else:
        genres_movie = None

    if genres_movie is not None:
        for genre in genres_movie:
            cursor.execute(f"select count(name_genre) from genre where name_genre = ('%s')" % genre)
            checkcount_genre = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]
            if checkcount_genre == conf.COUNT_ZERO:
                cursor.execute(f'''INSERT INTO genre (name_genre) VALUES (%s)''', genre)
            cursor.execute(f"select id_genre from genre where name_genre = ('%s')" % genre)
            id_genre = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]
            cursor.execute(f'''INSERT INTO movies_to_genre (movies_id_movies , genre_id_genre) VALUES (%s,%s)''',
                           (id_movie, id_genre))


def implement_writer(movie, cursor, id_movie):
    """
    insert all the writer  into the sql tables writer
    :param movie: dic with movie info
    :param cursor: sql cursor
    :return: id_movie
    """

    if 'Writer' in movie.keys():
        writers = movie['Writer'].replace("'", "`").split(',')
    else:
        writers = None

    if writers is not None:
        for writer in writers:
            cursor.execute(f"select count(name_writer) from writers where name_writer = ('%s')" % writer)
            checkcount_writer = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]
            if checkcount_writer == conf.COUNT_ZERO:
                cursor.execute(f'''INSERT INTO writers (name_writer) VALUES (%s)''', writer)
            cursor.execute(f"select id_writer from writers where name_writer = ('%s')" % writer)
            id_writer = cursor.fetchall()
            cursor.execute(
                f'''INSERT INTO movies_to_writers (movies_id_movies , writers_id_writer) VALUES (%s,%s)''',
                (id_movie, id_writer))


def implement_actors(movie, cursor, id_movie):
    """
    insert all the actors indo info the sql tables actors
    :param movie: dic with movie info
    :param cursor: sql cursor
    :return: id_movie
    """
    if 'actors' in movie.keys():
        actors = movie['actors'].replace("'", "`").split(',')
    else:
        actors = None

    if actors is not None:
        for actor in actors:
            cursor.execute(f"""select count(name_actor) from actors where name_actor = ('%s')""" % actor)
            checkcount_actor = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]
            if checkcount_actor == conf.COUNT_ZERO:
                cursor.execute(f'''INSERT INTO actors (name_actor) VALUES (%s)''', actor)
            cursor.execute(f"select id_actor from actors where name_actor = ('%s')" % actor)
            id_actor = cursor.fetchall()
            cursor.execute(f'''INSERT INTO movies_to_actors (movies_id_movies , actors_id_actor) VALUES (%s,%s)''',
                           (id_movie, id_actor))


def implement_producer(movie, cursor, id_movie):
    """
     insert all the producer info into the sql tables producer
    :param movie: dic with movie info
    :param cursor: sql cursor
    :return: id_movie
    """
    if 'Producer' in movie.keys():
        producers = movie['Producer'].replace("'", "`").split(',')
    else:
        producers = None

    if producers is not None:
        for producer in producers:
            cursor.execute(f"select count(name_producer) from producers where name_producer = ('%s')" % producer)
            checkcount_producer = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]
            if checkcount_producer == conf.COUNT_ZERO:
                cursor.execute(f'''INSERT INTO producers (name_producer) VALUES (%s)''', producer)
            cursor.execute(f"select id_producer from producers where name_producer = ('%s')" % producer)
            id_producer = cursor.fetchall()
            cursor.execute(
                f'''INSERT INTO movies_to_producers (movies_id_movies , producers_id_producer) VALUES (%s,%s)''',
                (id_movie, id_producer))


def implement_director(movie, cursor, id_movie):
    """
    insert all the director info into the sql tables director
    :param movie: dic with movie info
    :param cursor: sql cursor
    :return: id_movie
    """

    if 'Director' in movie.keys():
        directors = movie['Director'].replace("'", "`").split(',')
    else:
        directors = None

    if directors is not None:
        for director in directors:
            cursor.execute(f"select count(name_director) from directors where name_director = ('%s')" % director)
            checkcount_director = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]
            if checkcount_director == conf.COUNT_ZERO:
                cursor.execute(f'''INSERT INTO directors (name_director) VALUES (%s)''', director)
            cursor.execute(f"select id_director from directors where name_director = ('%s')" % director)
            id_director = cursor.fetchall()
            cursor.execute(
                f'''INSERT INTO movies_to_directors (movies_id_movies , directors_id_director) VALUES (%s,%s)''',
                (id_movie, id_director))


def implement_distributor(movie, cursor, id_movie):
    """
    insert all the distributor info into the sql tables distributor
    :param movie: dic with movie info
    :param cursor: sql cursor
    :return: id_movie
    """
    if 'Distributor' in movie.keys():
        distributors = movie['Distributor'].replace("'", "`").split(',')
    else:
        distributors = None

    if distributors is not None:
        for distributor in distributors:
            cursor.execute(
                f"select count(name_distributor) from distributors where name_distributor = ('%s')" % distributor)
            checkcount_distributor = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]
            if checkcount_distributor == conf.COUNT_ZERO:
                cursor.execute(f'''INSERT INTO distributors (name_distributor) VALUES (%s)''', distributor)
            cursor.execute(f"select id_distributor from distributors where name_distributor = ('%s')" % distributor)
            id_distributor = cursor.fetchall()
            cursor.execute(
                f'''INSERT INTO movies_to_distributors (movies_id_movies , distributors_id_distributor) VALUES (%s,%s)''',
                (id_movie, id_distributor))


def from_dict_to_database(total_movies, password):
    """
    connect to your sql database, and implement all your dic in movie inside
    :param total_movies: dic of all the movies with their data
    :param password: password of your sql account
    """

    cursor, connection = connect_to_database(password)
    cursor.execute('use rotten;')

    for movie in total_movies:

        if 'movies' in movie.keys():
            name_movie = movie['movies'].replace("'", "`")
        else:
            name_movie = None

        cursor.execute(f"select count(name_movie) from movies where name_movie = ('%s')" % name_movie)
        checkcount = cursor.fetchall()[conf.FIRST_ELEMENT][conf.FIRST_ELEMENT]

        if checkcount > conf.COUNT_ZERO:
            continue

        id_movie = implement_movie(movie, cursor, name_movie)
        implement_genre(movie, cursor, id_movie)
        implement_writer(movie, cursor, id_movie)
        implement_actors(movie, cursor, id_movie)
        implement_producer(movie, cursor, id_movie)
        implement_director(movie, cursor, id_movie)

    connection.commit()
    connection.close()


def trailer_url(movie_name):
    """
    by using the youtube api , find in youtube the trailer url of each movie
    :param movie_name: string name of the movie
    :return: a string which is the link of the trailer movie on youtube
    """
    trailer_movie_name = movie_name + ' trailer'
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={trailer_movie_name}&type=video&key=AIzaSyCzIQvUdexnVnmfw7lYqVufpeTGv8MAruE"
    response = requests.request("GET", url)
    end_url = json.loads(response.text)['items'][conf.FIRST_ELEMENT]['id']['videoId']
    url = 'https://www.youtube.com/watch?v=' + end_url
    return url


def main():
    args = sys.argv[conf.FIRST_ARGUMENT:]
    if len(args) < conf.NUMBER_OF_ARGUMENTS:
        print('usage: rotten_tomatoes_scrapper.py [category] [number of movies] [SQL PASSWORD] [chrome path driver] ')
        sys.exit(1)
    if args[conf.CATEGORY].upper() not in conf.URLS_NAME:
        print('choose a category from this list', conf.URLS_NAME)
        sys.exit(1)
    if not args[conf.NUMBER_OF_MOVIES].isnumeric():
        print('give us a digit please')
        sys.exit(1)
    password = args[conf.SQL_PASSWORD]
    chrome_path = args[conf.CHROME_PATH_DRIVER]
    if not ERD.verify_database(password):
        ERD.create_database(password)
    url = getattr(conf, 'URL_' + args[conf.ZERO].upper())
    movies = scrap_main_page(url, chrome_path)
    size_movies = min(len(movies), int(args[conf.NUMBER_OF_MOVIES]))
    total_movies = scrap_each_movie(movies, size_movies, chrome_path)
    from_dict_to_database(total_movies[: size_movies], password)


if __name__ == '__main__':
    main()

