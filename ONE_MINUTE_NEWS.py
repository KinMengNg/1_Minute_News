import pyttsx3
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
#import datetime

def talkToMe(audio):
    #speaks audio passed as argument
    print(audio)
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 130)     # setting up new voice rate
    engine.say(audio)
    engine.runAndWait()

#not using it here, usng it in the other filde
##def saveToFile(audio, country, date):
##    print(audio)
##    engine = pyttsx3.init()
##    rate = engine.getProperty('rate')   # getting details of current speaking rate
##    engine.setProperty('rate', 130)     # setting up new voice rate
##
##    name = f'{country}-{date}'
##    engine.save_to_file(audio, name)
##    engine.runAndWait()

#All country codes: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
country_codes = [('Singapore','SG'), ('Malaysia','MY'), ('United States','US'), ('United Kingdom','UK'), ('India','IN'), ('Australia','AU'), ('New Zealand', 'NZ'), ('South Africa', 'ZA')]


for country in country_codes:
    prompt = ''
    while prompt != 'y' and prompt != 'n':
        prompt = input(f'Would you like to hear the headlines of {country[0]} ? [Y/N]')

    if prompt.lower() == 'y':
        news_url=f'https://news.google.com/rss?hl=en-{country[1]}&gl={country[1]}&ceid={country[1]}:en'    #"https://news.google.com/news/rss"
        Client=urlopen(news_url)
        xml_page=Client.read()
        Client.close()

        soup_page=soup(xml_page,"xml")
        news_list=soup_page.findAll("item")
        # Print news title, url and publish date
        talkToMe(f"Here are some of today's headlines in {country[0]}")
        for news in news_list[:5]:
          talkToMe(news.title.text)
          print(news.link.text)
          print(news.pubDate.text)
          print("-"*60)
          print()
          print()
        talkToMe('And.')
        talkToMe(news_list[5].title.text)
        print("-"*60)
        print()
        print()
        
    elif prompt.lower() == 'n':
        continue

talkToMe('That is all')
