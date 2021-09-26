import pyttsx3
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen, Request
import time
import random

def talkToMe(audio):
    #speaks audio passed as argument
    print(audio)
    rate = random.randint(130,150) #so its not so monotonous
    print('RATE: ', rate)
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', rate)     # setting up new voice rate
    engine.say(audio)
    engine.runAndWait()

news_url= 'https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=6311'
page=Request(news_url,headers={'User-Agent': 'Mozilla/5.0'}) 
Client=urlopen(page)
xml_page=Client.read()
Client.close()

soup_page=soup(xml_page,"xml")
news_list=soup_page.findAll("item")
talkToMe('Here are the top world headlines.')
continuers = ['In other news.', 'Moving on.', 'Next up.', 'in the next headline.', 'following after that.']

for news in news_list:
    #if its not the first article, mention one of the random choice of cotinuer
    if news != news_list[0]:
        talkToMe(random.choice(continuers))
    
    title = str(news.title)[7:-8] #remove the <title> and </title>
    #print(title.upper())
    talkToMe(title)
    prompt = input('Would you like to hear about it in detail?[y/n]: ')

    if prompt == 'y':
        link = str(news.link)[6:-7] #remove <link> and </link>
        page = Request(link,headers={'User-Agent': 'Mozilla/5.0'})
        Client=urlopen(page)
        html_page=Client.read()
        Client.close()
        new_page = soup(html_page, 'lxml')
        paragraphs = new_page.findAll('p')
        useful_paragraphs = paragraphs[3:-5] #the rest are like headers and other subscription stuff
        for paragraph in useful_paragraphs:
            paragraph = str(paragraph)[3:-4] #without the <p> and </p>
            if 'subscribe to our Telegram channel' in paragraph:
                continue
            else:
                #if it has a link in it, remove it first
                if '<a' in paragraph and '</a>' in paragraph:
                    #find the first occurence for both
                    start_index = paragraph.index('<') 
                    end_index = paragraph.index('>')
                    paragraph = paragraph[:start_index] + paragraph[end_index+1:]

                    #then i need to remove the </a>, so do the same thing
                    start_index = paragraph.index('<') 
                    end_index = paragraph.index('>')
                    paragraph = paragraph[:start_index] + paragraph[end_index+1:]

                talkToMe(paragraph)
                print()
    else:
        pass
    
    print('----------------------------------------------')
    print()
    print()
    time.sleep(2)
