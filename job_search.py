import requests
from bs4 import BeautifulSoup
import re
import bs4 as bs
import json
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

text = urllib2.urlopen('http://dcsd.nutrislice.com/menu/meadow-view/lunch/').read()
menu = json.loads(re.search(r"bootstrapData\['menuMonthWeeks'\]\s*=\s*(.*);", text).group(1))

print menu

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
print(soup1)

for a in soup1.find_all("a", {"class": "item-details-link"}):
    if a.text:
        iid_links_with_text.append(a.text)


#print(iid_links_with_text)

