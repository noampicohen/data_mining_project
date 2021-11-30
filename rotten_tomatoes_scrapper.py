import csv
import time
import conf
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import sys
import pymysql
from datetime import datetime

INPUT_DRIVER = input(conf.INPUT_QUESTION)


def read_csv(file_path):
    file = open(file_path)
    csvreader = csv.reader(file)
    header = next(csvreader)
    total_movies = []
    for row in csvreader:
        dic = {}
        for i in range(len(row)):
            if row[i] != '':
                dic[header[i]] = row[i]
        total_movies.append(dic)
    file.close()
    return total_movies


def transform_box_office_to_number(box_office):
    """
        transform the number to box office from a string to an int
    """
    if box_office[-1] == 'K':
        return round(float(box_office[1: -1])) * 1000
    if box_office[-1] == 'M':
        return round(float(box_office[1: -1])) * 1000
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


def scrap_main_page(url):
    """
    :return: a list of dict containing name , release date , and link to the website of the movie.
    """
    movies = []
    driver = webdriver.Chrome(INPUT_DRIVER)
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


def scrap_each_movie(movies, size_movies):
    """

    :param movies: list of dict containing name and url of movies
    :return: list of dict  with all info needed added
    """

    for i in range(size_movies):
        url_movie = movies[i]["url_page"]
        try:
            info_movie = find_info(url_movie)
            movies[i].update(info_movie)
        except Exception:
            pass
    return movies


def find_info(url_movie):
    """

    :param url_movie: receive url of a movie
    :return: list with all info needed and found on the movie
    """
    actor_list = []
    driver = webdriver.Chrome('/Users/nissielthomas/Downloads/chromedriver')
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
        tomato_rate = rates[1].split('=')[1].replace("\"", "")
        audience_rate = rates[6].split('=')[1].replace("\"", "")
        info_movie['tomato_rate'] = tomato_rate
        info_movie['audience_rate'] = audience_rate

        actor_dict = []
        info_actors(soup, actor_dict, conf.HTML_ACTOR, actor_list)
        info_actors(soup, actor_dict, conf.HTML_ACTOR_HIDE, actor_list)

        info_movie['actors'] = ', '.join(actor_list)
        return info_movie
    except Exception:
        pass


def info_actors(soup, actor_dict, path, actor_list):
    """ in a specific page put in a list a dic with
    the name of the actors ,their role and a url who lead to the actor page"""

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
        name = result[0]
        dict['name'] = name.replace("'", "`")
        if len(result) > 1:
            role = result[1]
            dict['role'] = role
        actor_list.append(dict['name'])
        actor_dict.append(dict)


def from_dict_to_csv(total_movies):
    """
    write all the input dict into a csv
    """
    keys = set().union(*(d.keys() for d in total_movies))
    movies_file = open("movies.csv", "w")
    dict_writer = csv.DictWriter(movies_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(total_movies)
    movies_file.close()


def from_dict_to_database(total_movies, password):
    """
    connect to your sql database, and implement all your dic in movie inside
    """
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password=password)
    cursor = connection.cursor()
    cursor.execute('use rotten;')

    for movie in total_movies:
        if 'movies' in movie.keys():
            name_movie = movie['movies'].replace("'", "`")
        else:
            name_movie = None

        cursor.execute(f"select count(name_movie) from movies where name_movie = ('%s')" % name_movie)
        checkcount = cursor.fetchall()[0][0]
        if checkcount > 0:
            continue

        if 'Original Language' in movie.keys():
            language_movie = movie['Original Language']
        else:
            language_movie = None
        if 'synopsis' in movie.keys():
            if len(movie['synopsis']) >= 128:
                text_synopsis = movie['synopsis'][:128].replace("'", "`")
            else:
                text_synopsis = movie['synopsis'].replace("'", "`")
        else:
            text_synopsis = None
        if 'url_page' in movie.keys():
            url_page = movie['url_page']
        else:
            url_page = None
        if 'Release Date (Streaming)' in movie.keys():
            date_streaming = datetime.strptime(movie['Release Date (Streaming)'][:12].rstrip(), '%b %d, %Y').strftime(
                '%Y-%m-%d')
        else:
            date_streaming = None
        if 'Release Date (Theaters)' in movie.keys():
            date_theaters = datetime.strptime(movie['Release Date (Theaters)'][:12].rstrip(), '%b %d, %Y').strftime(
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

        if 'Genre' in movie.keys():
            genres_movie = movie['Genre'].replace("'", "`").split(',')
        else:
            genres_movie = None

        if 'Writer' in movie.keys():
            writers = movie['Writer'].replace("'", "`").split(',')
        else:
            writers = None

        if 'actors' in movie.keys():
            actors = movie['actors'].replace("'", "`").split(',')
        else:
            actors = None

        if 'Producer' in movie.keys():
            producers = movie['Producer'].replace("'", "`").split(',')
        else:
            producers = None

        if 'Director' in movie.keys():
            directors = movie['Director'].replace("'", "`").split(',')
        else:
            directors = None

        if 'Distributor' in movie.keys():
            distributors = movie['Distributor'].replace("'", "`").split(',')
        else:
            distributors = None

        # table language
        if language_movie is not None:
            cursor.execute(f'INSERT INTO languages (name_language) VALUES (%s)', language_movie)
            cursor.execute(f"select id_language from languages where name_language = ('%s')" % language_movie)
            id_language = cursor.fetchall()[0][0]
        if text_synopsis is not None:
            cursor.execute(f'''INSERT INTO synopsis (text_synopsis) VALUES (%s)''', text_synopsis)
            cursor.execute(f"""select id_synopsis from synopsis where text_synopsis = ('%s')""" % text_synopsis)
            id_synopsis = cursor.fetchall()[0][0]
        cursor.execute(
            f'INSERT INTO movies (name_movie,url_page,release_date_streaming ,release_date_theater ,rate_tomato,rate_audience ,boxoffice,languages_id_language,synopsis_id_synopsis) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            (name_movie, url_page, date_streaming, date_theaters, tomato_rate, audience_rate, box_office, id_language,
            id_synopsis))
        cursor.execute(f"select id_movies from movies where name_movie = ('%s')" % name_movie)
        id_movie = cursor.fetchall()[0][0]
        if genres_movie is not None:
            for genre in genres_movie:
                cursor.execute(f"select count(name_genre) from genre where name_genre = ('%s')" % genre)
                checkcount_genre = cursor.fetchall()[0][0]
                if checkcount_genre == 0:
                    cursor.execute(f'''INSERT INTO genre (name_genre) VALUES (%s)''', genre)
                cursor.execute(f"select id_genre from genre where name_genre = ('%s')" % genre)
                id_genre = cursor.fetchall()[0][0]
                cursor.execute(f'''INSERT INTO movies_to_genre (movies_id_movies , genre_id_genre) VALUES (%s,%s)''',
                               (id_movie, id_genre))

        if writers is not None:
            for writer in writers:
                cursor.execute(f"select count(name_writer) from writers where name_writer = ('%s')" % writer)
                checkcount_writer = cursor.fetchall()[0][0]
                if checkcount_writer == 0:
                    cursor.execute(f'''INSERT INTO writers (name_writer) VALUES (%s)''', writer)
                cursor.execute(f"select id_writer from writers where name_writer = ('%s')" % writer)
                id_writer = cursor.fetchall()
                cursor.execute(
                    f'''INSERT INTO movies_to_writers (movies_id_movies , writers_id_writer) VALUES (%s,%s)''',
                    (id_movie, id_writer))
        if actors is not None:
            for actor in actors:
                cursor.execute(f"""select count(name_actor) from actors where name_actor = ('%s')""" % actor)
                checkcount_actor = cursor.fetchall()[0][0]
                if checkcount_actor == 0:
                    cursor.execute(f'''INSERT INTO actors (name_actor) VALUES (%s)''', actor)
                cursor.execute(f"select id_actor from actors where name_actor = ('%s')" % actor)
                id_actor = cursor.fetchall()
                cursor.execute(f'''INSERT INTO movies_to_actors (movies_id_movies , actors_id_actor) VALUES (%s,%s)''',
                               (id_movie, id_actor))

        if producers is not None:
            for producer in producers:
                cursor.execute(f"select count(name_producer) from producers where name_producer = ('%s')" % producer)
                checkcount_producer = cursor.fetchall()[0][0]
                if checkcount_producer == 0:
                    cursor.execute(f'''INSERT INTO producers (name_producer) VALUES (%s)''', producer)
                cursor.execute(f"select id_producer from producers where name_producer = ('%s')" % producer)
                id_producer = cursor.fetchall()
                cursor.execute(
                    f'''INSERT INTO movies_to_producers (movies_id_movies , producers_id_producer) VALUES (%s,%s)''',
                    (id_movie, id_producer))

        if directors is not None:
            for director in directors:
                cursor.execute(f"select count(name_director) from directors where name_director = ('%s')" % director)
                checkcount_director = cursor.fetchall()[0][0]
                if checkcount_director == 0:
                    cursor.execute(f'''INSERT INTO directors (name_director) VALUES (%s)''', director)
                cursor.execute(f"select id_director from directors where name_director = ('%s')" % director)
                id_director = cursor.fetchall()
                cursor.execute(
                    f'''INSERT INTO movies_to_directors (movies_id_movies , directors_id_director) VALUES (%s,%s)''',
                    (id_movie, id_director))

        if distributors is not None:
            for distributor in distributors:
                cursor.execute(
                    f"select count(name_distributor) from distributors where name_distributor = ('%s')" % distributor)
                checkcount_distributor = cursor.fetchall()[0][0]
                if checkcount_distributor == 0:
                    cursor.execute(f'''INSERT INTO distributors (name_distributor) VALUES (%s)''', distributor)
                cursor.execute(f"select id_distributor from distributors where name_distributor = ('%s')" % distributor)
                id_distributor = cursor.fetchall()
                cursor.execute(
                    f'''INSERT INTO movies_to_distributors (movies_id_movies , distributors_id_distributor) VALUES (%s,%s)''',
                    (id_movie, id_distributor))

    connection.commit()
    connection.close()


def main():
    args = sys.argv[1:]
    if len(args) < 3:
        print('usage: rotten_tomatoes_scrapper.py [category] [number of movies] [SQL PASSWORD] ')
        sys.exit(1)
    if args[0].upper() not in conf.URLS_NAME:
        print('choose a category from this list', conf.URLS_NAME)
        sys.exit(1)
    if not args[1].isnumeric():
        print('give us a digit please')
        sys.exit(1)
    password = args[2]
    url = getattr(conf, 'URL_' + args[0].upper())
    movies = scrap_main_page(url)
    size_movies = min(len(movies), int(args[1]))
    total_movies = scrap_each_movie(movies, size_movies)

    """If we want to print all our movies into a csv_file"""
    # from_dict_to_csv(total_movies)
    """If we want to create a database from a csv file """
    # total_movies = read_csv('movies1.csv')

    from_dict_to_database(total_movies, password)


if __name__ == '__main__':
    main()
