#  pip3 install requests beautifulsoup4 lxml selenium
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def cleanString(name):
    return name.replace(' ', '%20')

def cleanFloat(number):
    return number.replace(',', '.')

def scrapingMovies(listMovies = []):
    for theMovie in listMovies:
        driver.get('http://www.allocine.fr/recherche/movie/?q='+cleanString(theMovie['title']))
        dataParse = BeautifulSoup(driver.page_source, "lxml")
        section = dataParse.find("section", {"class": 'section movies-results'})
        moviesResults = section.findAll("li", {"class": 'mdl'})
        if len(moviesResults) == 0 or len(moviesResults) > 1:
            continue
        else:
            # print(moviesResults[0].find('a'))
            getMovie(moviesResults[0].find('a').attrs['href'])
    #saveData(bdd)

def getMovie(url = ''):
    driver.get('http://www.allocine.fr'+url)
    dataParse = BeautifulSoup(driver.page_source, "lxml")
    # # CardMovie = dataParse.find("div", {"class": 'gd-col-left'}).find("div", {"class": 'card entity-card entity-card-overview entity-card-list cf '})
    divLeft = dataParse.find("div", {"class": 'gd-col-left'})
    CardMovie = divLeft.findChildren("div")[1]

    # print(CardMovie)
    listGenres = CardMovie.find('div', {'class': 'meta-body-item meta-body-info'}).findAll("a", {"class": 'xXx'})

    genres = []

    for i in range(1, len(listGenres)):
        genres.append(listGenres[i].text)

    print(genres)

    nationality = CardMovie.findAll('div', {'class': 'meta-body-item'})[-1].find("a", {"class": 'xXx'}).text

    print(nationality)

    listRate = CardMovie.findAll('div', {'class': 'rating-item-content'})
    rates = [rate.find('span', {'class': 'stareval-note'}).text for rate in listRate if rate.find('span', {'class': 'stareval-note'}).text != '--']

    rate = len(rates) < 2 and (float(cleanFloat(rates[0]))*4+10)/2 or (float(cleanFloat(rates[0]))*4+float(cleanFloat(rates[1]))*4)/2
    print( rate)


def saveData(data):
    with open('scraping.json', 'w+', encoding='utf-8') as outfile:
        json.dump(data, outfile)
    

if __name__ == "__main__":
    chrome = webdriver.ChromeOptions()
    chrome.add_argument('--window-size=1920,1080')
    chrome.add_argument('--headless')
    chrome.add_argument('--disable-gpu')
    # Mac => brew cask install chromedriver
    # Win => driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe', options=chrome)
    driver = webdriver.Chrome(options=chrome)
    scrapingMovies([{ 'title': 'BORUTO : NARUTO, LE FILM', 'real': 'real'}])
    driver.close()