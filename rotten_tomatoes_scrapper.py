from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

import csv

url = "https://www.rottentomatoes.com/browse/in-theaters/"


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


def scrap_main_page():
    """
    :return: a list of dict containing name , release date , and link to the website of the movie.
    """
    movies = []
    driver = webdriver.Chrome("/Users/nissielthomas/Downloads/chromedriver")
    driver.get(url)
    click_more = driver.find_element(By.XPATH, '//*[@id="show-more-btn"]/button')
    # load all the main pages until the end
    while check_exists_by_xpath(driver, '//*[@id="show-more-btn"]/button'):
        click_more.click()
        time.sleep(2)

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    count = 0

    # find all the atributes needed from the main page and put it in a list of dict
    for element in soup.findAll('div', attrs={'class': 'movie_info'}):
        count += 1
        dic = {}
        title = element.find('h3', attrs={'class': 'movieTitle'})
        # release_date = element.find('p', attrs={'class': 'release-date'})
        url_page = element.find("a")['href']
        dic["movies"] = title.text
        # dic["release_date"] = release_date.text
        dic["url_page"] = "https://www.rottentomatoes.com" + url_page
        movies.append(dic)
    driver.quit()
    return movies


def scrap_each_movie(movies):
    """

    :param movies: list of dict containing name and url of movies
    :return: list of dict  with all info needed added
    """
    """
    try :
        Parallel(n_jobs=-1)(delayed(find_info)(movies[i]["url_page"]) for i in range(len(movies)))
    except Exception:
        pass
"""

    for i in range(0, 5):
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
    driver = webdriver.Chrome("/Users/nissielthomas/Downloads/chromedriver")
    driver.get(url_movie)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
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
        info_actors(soup, actor_dict, 'cast-item media inlineBlock', actor_list)
        info_actors(soup, actor_dict, 'cast-item media inlineBlock moreCasts hide', actor_list)

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
            dict['url'] = "https://www.rottentomatoes.com" + url_page
        except Exception:
            continue
        temp = element.text.splitlines()
        result = []
        [result.append(x.strip()) for x in temp if x.strip() != ""]
        name = result[0]
        dict['name'] = name
        if len(result) > 1:
            role = result[1]
            dict['role'] = role
        actor_list.append(dict['name'])
        actor_dict.append(dict)


def from_dict_to_csv(total_movies):
    keys = total_movies[0].keys()
    movies_file = open("movies.csv", "w")
    dict_writer = csv.DictWriter(movies_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(total_movies)
    movies_file.close()


def main():
    movies = scrap_main_page()
    total_movies = scrap_each_movie(movies)
    from_dict_to_csv(total_movies)


if __name__ == '__main__':
    main()
