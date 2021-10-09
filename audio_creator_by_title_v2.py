#########################################################
'''
RUN FROM CMD AS WELL,
JUST OPEN POWERSHELL FROM THE FOLDERTO RUN IT
NEED TO FOR THE TIMED INPUT TO WORK




'''
########################################################
import pyttsx3
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import datetime
import os
import shutil
from time import sleep
from threading import Thread
from inputimeout import inputimeout, TimeoutOccurred
from fake_useragent import UserAgent

#these only workswith selenium 4.0 alpha
##from selenium import webdriver
##from selenium.webdriver.edge.options import Options
##from selenium.webdriver.edge.service import Service
##from selenium.webdriver.edge.webdriver import WebDriver

#i currently have dselenium 3.141 which needs this to work
from msedge.selenium_tools import Edge, EdgeOptions

#USING EDGE
#returns actual link, not the google url
def getScreenShotandLink(link, country, title, date):
    driveroptions = EdgeOptions()

    #create a fake user agent to fool websites to know im not a bot
    ua = UserAgent()
    agent = ua.random
    driveroptions.add_argument(f'user-agent={agent}')

    # remember to set use_chromium
    driveroptions.use_chromium = True
    driveroptions.add_argument('--start-maximized')

    #wth this dontneed to install exntnesion every fcking time anymore woohoo
    driveroptions.add_argument(r'user-data-dir=D:\PROJECTS\1_MINUTE_NEWS\edge_selenium_profile')
    
    driveroptions.binary_location = r"c:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

    driver = Edge(options=driveroptions, executable_path=r'd:\Python3.7\msedgedriver.exe')
    driver.get(link)
    sleep(1)
    name = f'{country}_{title}_{date}.png'
    driver.get_screenshot_as_file(name)
    url = driver.current_url
    
    driver.quit() #closes the window

    return url

#USING FIREFOX
##def getScreenShotandLink(link, country, title, date):
##    #driveroptions = Options()
##    #driveroptions.add_argument('--start-maximized')
##    #driveroptions.binary_location = r"D:\FireFox\firefox.exe"
##    driver = webdriver.Firefox(executable_path=r'D:\PROJECTS\1_MINUTE_NEWS\geckodriver-v0.29.1-win64\geckodriver.exe')
##    driver.get(link)
##    sleep(1)
##    name = f'{country}_{title}_{date}.png'
##    driver.get_screenshot_as_file(name)
##    url = driver.current_url
##    
##    driver.quit() #closes the window
##
##    return url

def talkToMe(audio):
    #speaks audio passed as argument
    print(audio)
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 140)     # setting up new voice rate
    engine.say(audio)
    engine.runAndWait()

def saveToFile(audio, country, title, date):
    print(audio)
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 140)     # setting up new voice rate

    name = f'{country}_{title}_{date}.mp3'
    #path = f'/{date}/{name}'
    engine.save_to_file(audio, name)
    engine.runAndWait()



#All country codes: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
country_codes = [('Singapore','SG'), ('Malaysia','MY'), ('United States','US'), ('United Kingdom','UK'), ('India','IN'), ('Australia','AU'), ('New Zealand', 'NZ'), ('South Africa', 'ZA'), ('Indonesia', 'ID')]

date = str(datetime.date.today()) #todays date

#make a folder to put all todays date into it
if not os.path.exists(date):
    os.mkdir(date)

if not os.path.exists(f'{date}/videos'):
    os.mkdir(f'{date}/videos')#for the videos later, just create here easier
    

for country in country_codes:
    prompt = '' 
    counter = 0
    links = []
    titles = []
    while prompt != 'y' and prompt != 'n':
        #without timeout
        #prompt = input(f'Would you like to hear the headlines of {country[0]} ? [y/n]')

        #with timeout
        try:
            prompt = inputimeout(prompt=f'Would you like to hear the headlines of {country[0]} ? [y/n]: ', timeout=5)
        except TimeoutOccurred:
            print('Timed Out! Defaulting to Yes.')
            prompt = 'y'

    if prompt.lower() == 'y':
        #check if its already been done, if it has, skip
        if os.path.exists(f'{date}/{country[0]}_{date}.txt'):
            continue
        else:
            news_url=f'https://news.google.com/rss?hl=en-{country[1]}&gl={country[1]}&ceid={country[1]}:en'    #"https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()

            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            # Print news title, url and publish date
            #talkToMe(f"Here are some of today's headlines in {country[0]}")

##            #i only need to create this oce, which i already did
##            intro = f"Here are some of today's headlines in {country[0]}.\n"
##            saveToFile(intro, country[0],'Intro', date)
            
            for news in news_list[:9]:
              title = ''
              title += news.title.text + '\n'
              title_to_insert = str(news.title.text)
              title_to_insert = title_to_insert.replace('"', "'", 999)
              titles.append(title_to_insert)
              saveToFile(title, country[0], counter, date) #saving each file by title
              
              link = news.link.text
              actual_link = getScreenShotandLink(link, country[0], counter, date)
              links.append(actual_link)
              counter += 1
              
              
            title = ('And.\n') + (news_list[9].title.text) + '\n'
            title_to_insert = str(news_list[9].title.text)
            title_to_insert = title_to_insert.replace('"', "'", 999)
            titles.append(title_to_insert)
            link = news_list[9].link.text
            saveToFile(title, country[0], counter, date)
            actual_link = getScreenShotandLink(link, country[0], counter, date)
            links.append(actual_link)

            #add the links a=to a text file
            with open(f'{country[0]}_{date}.txt','w', encoding='utf-8') as f1:
                f1.write('Here are the links to the headlines in this video:\\n\\n')

                #titles and links should be same length and corresponding
                for i in range(len(links)):
                    f1.write(titles[i] + ':\\n' + links[i] + '\\n\\n') #the \\ is needed for the json file in the video uploading

            ##Move all the files fro the root folderinto its correct date folder
            #i put after everything is done to prevent it from crashing the program
            for file in os.listdir():
                if date in file and country[0] in file and ('.mp3' in file or '.png' in file or '.txt' in file):
                    shutil.move(file, f'{date}')
            
        print(f'Done with {country[0]}')
        
    elif prompt.lower() == 'n':
        continue
    
talkToMe('That is all')
