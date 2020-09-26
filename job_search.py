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

soup = requests.get("https://hr.imperialcounty.org/job-openings/", headers=headers)
soup1 =BeautifulSoup(soup.content,"lxml")
#print(soup1)


imperial_county_links_with_text = []
for a in soup1.findAll("a", {"class": "brz-cp-color2"}):
    if a.text != ' ':
        imperial_county_links_with_text.append(a.text)

#print(links_with_text)

with open('Job_search_in_Imperial.csv', 'w') as outFile:
    outFile.write('IMPERIAL COUNTY' + "\n")
    outFile.write('--------------------------' + "\n")
    for i in imperial_county_links_with_text:
        outFile.write(i + "\n")

soup = requests.get('https://www.icoe.org/jobs', headers = headers)
soup1 =BeautifulSoup(soup.content,"lxml")
#print(soup1)

icoe_links_with_text = []

icoe = soup1.find("a", href=re.compile("DistrictJob"))
icoe = soup1.find_all("a", href=lambda href: href and "DistrictJob" in href)

for a in soup1.findAll("a", href=lambda href: href and "DistrictJob" in href):
    if a.text != ' ':
        icoe_links_with_text.append(a.text)

#print(icoe_links_with_text)


with open('Job_search_in_Imperial.csv', 'a') as outFile:
    outFile.write('\n' + "\n")
    outFile.write('Imperial County Office of Education' + "\n")
    outFile.write('--------------------------' + "\n")
    for i in icoe_links_with_text:
        outFile.write(i + "\n")


soup = requests.get('https://www.governmentjobs.com/careers/iid')
soup1 =BeautifulSoup(soup.content,"lxml")
iid_links_with_text = []


for a in soup1.find_all("a", {"class": "item-details-link"}):
    if a.text:
        iid_links_with_text.append(a.text)

driver = webdriver.Chrome(executable_path='C:\\Users\\Ben\\Documents\\ECESD-Scripts-master\\chromedriver_win32\\chromedriver')




schools_dict = {'https://www.edjoin.org/besd':'Brawley Elementary School District','https://www.edjoin.org/Home/Jobs?stateID=24&countyID=13&districtID=6371':'Calexico Unified School District Personnel Commision','https://www.edjoin.org/ECESD':'El Centro Elementary School District','https://www.edjoin.org/buhsd':'Brawley Union High School District','https://www.edjoin.org/calexico':'Calexico Unified School District','https://www.edjoin.org/calipatria': 'Calipatria Unified'
           ,'https://www.edjoin.org/CentralUnionHSD':'Central Union High School District','https://www.edjoin.org/heberschooldistrict':'Heber Elementary','https://www.edjoin.org/holtvilleusd':'Heber Elementary','https://www.edjoin.org/imperialusd':'Imperial Unified School District'
                ,'https://www.edjoin.org/Home/Jobs?stateID=24&countyID=13&districtID=208':'Holtville Unified School District'}


SchoolDistrict_links_with_text = []

driver.get('https://www.edjoin.org/besd')
time.sleep(3)
try:
    display = driver.find_element_by_xpath('/html/body/div[3]/section/section/div[10]/article[2]/div[2]/div[1]/select')
except:
    print('exception found!')
    driver.find_element_by_xpath('/html/body/div[5]/div/div/div[2]/button[1]').click()
    pass

delay = 6
try:
   myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-job-title')))
   print("Page is ready!")
except TimeoutException:
   print("Loading took too much time!")
display.click()
display.send_keys('50')
display.send_keys(Keys.ENTER)
time.sleep(3)



for i,v in schools_dict.items():

    driver.get(i)
    time.sleep(3)




    delay = 3  # seconds
    if v != 'Calexico Unified School District Personnel Commision':
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-job-title')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
            #myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'footable-visible footable-first-column')))
        jobs = driver.find_elements_by_class_name('card-job-title')

        for job in jobs:
            SchoolDistrict_links_with_text.append(job.text)

        with open('Job_search_in_Imperial.csv', 'a') as outFile:

            outFile.write('\n' + "\n")
            outFile.write(v + "\n")
            outFile.write('--------------------------' + "\n")
            for i in SchoolDistrict_links_with_text:
                outFile.write(i + "\n")

        SchoolDistrict_links_with_text = []


    if v == 'Calexico Unified School District Personnel Commision':
        time.sleep(3)
        jobs = driver.find_elements_by_xpath('//a[contains(@href,"/Home/DistrictJobPosting/")]')

        for job in jobs:
            SchoolDistrict_links_with_text.append(job.text)

        with open('Job_search_in_Imperial.csv', 'a') as outFile:

            outFile.write('\n' + "\n")
            outFile.write(v + "\n")
            outFile.write('--------------------------' + "\n")
            for i in SchoolDistrict_links_with_text:
                outFile.write(i + "\n")

        SchoolDistrict_links_with_text = []