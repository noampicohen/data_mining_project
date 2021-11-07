#test1
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

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
        release_date = element.find('p', attrs={'class': 'release-date'})
        url_page = element.find("a")['href']
        dic["movies"] = title.text
        dic["release_date"] = release_date.text
        dic["url_page"] = "https://www.rottentomatoes.com" + url_page
        movies.append(dic)
    print(count)
    driver.quit()
    return movies


def scrap_each_movie(movies):
    for i in range(len(movies)):
        url_movie = movies[i]["url_page"]
        find_info(url_movie)


def find_info(url_movie):
    driver = webdriver.Chrome("/Users/nissielthomas/Downloads/chromedriver")
    driver.get(url_movie)
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    


def main():
    movies = scrap_main_page()
    total_movies = scrap_each_movie(movies)
    # for i in range(len(movies)):
    # print(movies[i]["url_page"])


if __name__ == '__main__':
    main()
