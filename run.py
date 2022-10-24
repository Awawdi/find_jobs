from datetime import date
import json
from os import path
import os
import requests
from bs4 import BeautifulSoup

today = str(date.today())
filename = "C:\\Users\\oawawdi\\Documents\\python coding\\Redis\\Redis\\jobs.json"
listObj = []
jobs=[]
latest_jobs=[]
elements = []


def find_delta_jobs(listObj):
    latest_jobs = listObj[-1]["jobs"]
    last_job_date = str(listObj[-1]["date"])

    delta_jobs = set(jobs)-set(latest_jobs)
    if len(delta_jobs)>0:
        print(f"{len(delta_jobs)} were added, comparing {last_job_date} and {today}:")
    for new_job in delta_jobs:
        print(new_job)

def write_new_jobs():
    dictionary = {
    "date": today,
    "number_of_jobs": len(elements),
    "jobs": jobs}

    listObj.append(dictionary)
    return listObj

def is_file_empty():
    """ Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty
    return os.path.exists(filename) and os.stat(filename).st_size == 0

url = 'https://www.careerarc.com/job-search?campaign_id=69733'
response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')
elements = soup.find_all('div', class_='job-posting-item')
if elements:
    print(f"{len(elements)} jobs were found:")
    for element in elements:
        if element.find('h2').a.text:
            job = element.find('h2').a.text
            jobs.append(job)
            print(job)
else:
    print(f"no jobs were found for today {today}.")

# Read JSON file
try:
    with open(filename,'w+') as fp:
        if not is_file_empty():
            listObj = json.load(fp)
            find_delta_jobs(listObj)
        new_listObj = write_new_jobs()
        json.dump(new_listObj, fp, 
                        indent=4,  
                        separators=(',',': '))

except ValueError:
    print('Loading JSON has failed')
