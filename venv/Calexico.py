
import time
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from selenium.webdriver.support.wait import WebDriverWait

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})
driver = webdriver.Chrome(executable_path='C:\\Users\\Ben\\Documents\\ECESD-Scripts-master\\chromedriver_win32\\chromedriver')
driver.get('https://www.edjoin.org/Home/Jobs?stateID=24&countyID=13&districtID=6371')
time.sleep(3)
calexico = driver.find_elements_by_xpath('//a[contains(@href,"/Home/DistrictJobPosting/")]')

for i in calexico:
    print(i.text)

#//*[@id="tblJobs"]/tbody/tr[2]/td[1]/b[1]/a

#//*[@id="tblJobs"]/tbody/tr[3]/td[1]/b[1]/a