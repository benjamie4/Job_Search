import time
import driver as driver
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

# Grabs job data from Imperial County website
soup = requests.get("https://hr.imperialcounty.org/job-openings/", headers=headers)
soup1 = BeautifulSoup(soup.content, "lxml")

# Creates a list of the jobs listed on the website
imperial_county_links_with_text = []
for a in soup1.findAll("a", {"class": "brz-cp-color2"}):
    if a.text != ' ':
        imperial_county_links_with_text.append(a.text)


# This function ensures that the CSV file will erase previous data
def write_jobs_alpha(Employer, List):
    with open('Job_search_in_Imperial.csv', 'w') as outFile:
        outFile.write(Employer + "\n")
        outFile.write('--------------------------' + "\n")
        for i in List:
            outFile.write(i + "\n")


# This function appends the data after write_jobs_alpha function
def write_jobs(Employer, List):
    with open('Job_search_in_Imperial.csv', 'a') as outFile:
        outFile.write('\n' + "\n")
        outFile.write(Employer + "\n")
        outFile.write('--------------------------' + "\n")
        for i in List:
            outFile.write(i + "\n")

write_jobs_alpha('Imperial County', imperial_county_links_with_text)


# Starts selenium webdriver for javascript pages on Edjoin
driver = webdriver.Chrome(executable_path='C:\\Users\\besquivel\\Documents\\Job_Search\\Chromedriver')

# California State Jobs
california_state_job_list = []
driver.get('https://www.calcareers.ca.gov/CalHRPublic/Search/JobSearchResults.aspx#locid=122')
time.sleep(6)
#driver.find_element_by_xpath("//select[@name='ctl00$cphMainContent$ddlRowCount']/option[text()='100']").click()
select = Select(driver.find_element_by_name('ctl00$cphMainContent$ddlRowCount'))
select.select_by_visible_text('100 Jobs')
time.sleep(5)
#jobs = driver.find_elements_by_id('cphMainContent_rptResults_hlViewJobPosting_' + '1')
i = 1
jobs = driver.find_elements_by_xpath('cphMainContent_rptResults_hlViewJobPosting_' + str(i))
# TODO: Finish troubleshooting getting california jobs

write_jobs('State of California', california_state_job_list)



# Brawley Job Openings
Brawley_Job_List = []
driver.get('http://www.brawley-ca.gov/section/Personnel/Job-Openings')
jobs = driver.find_elements_by_xpath('//a[contains(@href,"cms/kcfinder/upload/files")]')
for job in jobs:
    Brawley_Job_List.append(job.text)

write_jobs('City of Brawley', Brawley_Job_List)


# Grabs job data from City of Imperial Website
soup = requests.get("https://agency.governmentjobs.com/imperialca/default.cfm", headers=headers)
soup1 = BeautifulSoup(soup.content, "lxml")

# Creates a list of the jobs listed on the website
city_of_imperial_jobs = []
for a in soup1.findAll("a", {"class": "jobtitle"}):
    if a.text != ' ':
        city_of_imperial_jobs.append(a.text)


write_jobs('City of Imperial', city_of_imperial_jobs)


# Grabs job data from City of Imperial Website
soup = requests.get("https://www.governmentjobs.com/careers/imperialcourts", headers=headers)
soup1 = BeautifulSoup(soup.content, "lxml")

# Creates a list of the jobs listed on the website
superior_court_jobs = []

driver.get('https://www.governmentjobs.com/careers/imperialcourts/')
time.sleep(2)
jobs = driver.find_elements_by_xpath('//a[contains(@href,"careers/imperialcourts/jobs")]')
for job in jobs:
    job = job.text
    superior_court_jobs.append(job)
    print(job)

write_jobs('California Superior Court of California, Imperial County', superior_court_jobs)

# Key-Value Pair of school websites and school names
schools_dict = {'https://www.edjoin.org/besd': 'Brawley Elementary School District',
                'https://www.edjoin.org/Home/Jobs?stateID=24&countyID=13&districtID=6371': 'Calexico Unified School District Personnel Commision',
                'https://www.edjoin.org/ECESD': 'El Centro Elementary School District',
                'https://www.edjoin.org/buhsd': 'Brawley Union High School District',
                'https://www.edjoin.org/calexico': 'Calexico Unified School District',
                'https://www.edjoin.org/calipatria': 'Calipatria Unified',
                'https://www.edjoin.org/CentralUnionHSD': 'Central Union High School District',
                'https://www.edjoin.org/heberschooldistrict': 'Heber Elementary',
                'https://www.edjoin.org/icoe':'Imperial County Office of Education',
                'https://www.edjoin.org/holtvilleusd': 'Holtville Unified School District',
                'https://www.edjoin.org/imperialusd': 'Imperial Unified School District',
                'https://www.edjoin.org/Home/Jobs?stateID=24&countyID=13&districtID=4228': 'Imperial Valley College',
                'https://www.edjoin.org/meadowsunion': 'Meadows Union School District'
                }

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

# This loop goes through the school district list and grabs job postings
for i, v in schools_dict.items():

    driver.get(i)
    time.sleep(3)
    # TODO: Delete extra spacing
    if v == 'Calexico Unified School District Personnel Commision':
        time.sleep(3)
        jobs = driver.find_elements_by_xpath('//a[contains(@href,"/Home/DistrictJobPosting/")]')
        for job in jobs:
            job = job.text
            SchoolDistrict_links_with_text.append(job)

        write_jobs(v, SchoolDistrict_links_with_text)
        SchoolDistrict_links_with_text = []

    # TODO: Delete extra spacing
    if v == 'Imperial Valley College':
        time.sleep(3)
        jobs = driver.find_elements_by_xpath('//a[contains(@href,"/Home/DistrictJobPosting/")]')

        for job in jobs:
            SchoolDistrict_links_with_text.append(job.text)

        write_jobs('Imperial Valley College', SchoolDistrict_links_with_text)

        SchoolDistrict_links_with_text = []

    delay = 3  # seconds
    if v != 'Calexico Unified School District Personnel Commision' and v != 'Imperial Valley College':
        try:
            myElem = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'card-job-title')))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")
        jobs = driver.find_elements_by_class_name('card-job-title')

        for job in jobs:
            SchoolDistrict_links_with_text.append(job.text)

        write_jobs(v, SchoolDistrict_links_with_text)
        SchoolDistrict_links_with_text = []

