import argparse, os, time
import urllib.parse, random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')

#Search for link in page with attributes href
def getPeopleLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if 'profile/view?id=' in url:
                links.append(url)
    return links

#Search for jobs in page with attribute href
def getJobLinks(page):
    links = []
    for link in page.find_all('a'):
        url = link.get('href')
        if url:
            if '/jobs' in url:
                links.append(url)
    return links
#Get the ID of links
def getID(url):
    pUrl = urlparse.urlparse(url)
    return urlparse.parse_qs(pUrl.query) ['id'][0]

#Visit link and add visited link to an array
#Visit link if it's not in the list already
def ViewBot(browser):
    visited = {}
    pList = []
    count = 0
    while True:
        time.sleep(random.uniform(3.5, 6.9))
        page = BeautifulSoup(browser.page_source)
        people = getPeopleLinks(page)
        if people:
            for person in people:
                ID = getID(person)
                if ID not in visited:
                    pList.append(person)
                    visited[ID] = 1
        if pList:
            person = pList.pop()
            browser.get(person)
            count +=1
        else: 
            jobs = getJobLinks(page)
            if jobs:
                job = random.choice(jobs)
                root = 'http://www.linkedin.com'
                roots = 'http://www.linkedin.com'
                if root not in job or roots not in job:
                    job = 'https://www.linkedin.com' + job
                browser.get(job)
            else:
                print ("I'm lost. Exiting")
                break
        print ("[+] "+browser.title+" Visited! \n("\
			+str(count)+"/"+str(len(pList))+") Visited/Queue)")

def Main():
    #Parse as argument login email and password
    parser = argparse.ArgumentParser()
    parser.add_argument('email', help='linkedin email')
    parser.add_argument('password', help='linkedin password')
    args = parser.parse_args()

    #Navigate to login page
    browser = webdriver.Firefox()
    browser.get('https://linkedin.com/uas/login')

    #Search for id form
    emailElement = browser.find_element_by_id('session_key-login')
    emailElement.send_keys(args.email)
    passElement = browser.find_element_by_id('session_password-login')
    passElement.send_keys(args.password)
    passElement.submit()

    #Initialise ViewBot
    os.system('clear') #cls rather than clear on windows
    print ("[+] Success! Logged In, Bot Starting")
    ViewBot(browser)
    browser.close()

if __name__== "__main__":
    Main()

