import time
from bs4 import BeautifulSoup
import lxml
import requests
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions

FORM_ADDRESS = 'https://docs.google.com/forms/d/e/1FAIpQLSeGgVKbVACAAd9iIU_IN3PkTjhr-0C9omCuHbAjI-AMu2xU4A/viewform?usp=sf_link'
ZILLOW_URL = 'https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D'
headers = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}
response = requests.get(url=ZILLOW_URL, headers=headers)
zillow_web_addr = response.text
soup = BeautifulSoup(zillow_web_addr, "lxml")

prices = soup.find_all(name="div", class_="list-card-price")
links = soup.find_all(name="a", class_="list-card-link")
addresses = soup.find_all(name="address", class_="list-card-addr")

s = Service('/Users/shakayahaya/Desktop/chromedriver')

driver = webdriver.Chrome(service=s)
driver.get(FORM_ADDRESS)
time.sleep(5)
main_page = driver.current_window_handle
time.sleep(5)


def post_data_to_google_form():
    for price, link, address in zip(prices, links, addresses):
        address_form = driver.find_element(By.XPATH,
                                           '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        time.sleep(5)
        rent_form = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        time.sleep(5)
        link_form = driver.find_element(By.XPATH,
                                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        if price == prices[-1]:
            print("list is empty")
        else:
            try:
                time.sleep(10)
                address_form.send_keys(address.getText())
                time.sleep(3)
                rent_form.send_keys(price.getText())
                time.sleep(3)
                link_form.send_keys(link.get("href"))
                time.sleep(5)
                driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span').click()
                time.sleep(5)
                driver.find_element(By.CSS_SELECTOR, '.freebirdFormviewerViewResponseLinksContainer a').click()
            except WebDriverException:
                pass


post_data_to_google_form()
time.sleep(600)
