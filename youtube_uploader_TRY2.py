from youtube_uploader_selenium import YouTubeUploader
import datetime
import os
import shutil
from inputimeout import inputimeout, TimeoutOccurred

##########################
#I edited quite abit of the init file of youtube_uploader_selenium, including adding pyautogui to it
#
#########################

#get some of the required parameters so i can automate this shit
country_codes = [('Singapore','SG'), ('Malaysia','MY'), ('United States','US'), ('United Kingdom','UK'), ('India','IN'), ('Australia','AU'), ('New Zealand', 'NZ'), ('South Africa', 'ZA'), ('Indonesia', 'ID')]
date = str(datetime.date.today()) #todays date, is my path to folder too

#to check if the date folder exist, if its not, let me input it
if not os.path.exists(date):
    date = input(f'The date {date} folder does not exist, please insert another date manually: ')

for country in country_codes:
    prompt = ''#ask if i want to upload for each country
    
    while prompt != 'y' and prompt != 'n':
        #without timeout
        #prompt = input(f'Would you like to upload video for {country[0]} ? [Y/N]')

        #with timeout
        try:
            prompt = inputimeout(prompt=f'Would you like to upload video for {country[0]} ? [y/n]: ', timeout=5)
        except TimeoutOccurred:
            print('Timed Out! Defaulting to Yes.')
            prompt = 'y'
            
    if prompt.lower() == 'y':
        #check if its already been done, if it has, skip
        if os.path.exists(f'{date}/{country[0]}_{date}.json'):
            continue
        else:
            filepath = f'{date}/videos/{country[0]}_{date}_video.mp4'
            title = f'{country[0]} {date} -- 1 Minute News'
            with open(f'{date}/{country[0]}_{date}.txt','r', encoding='utf-8') as f1:
                description = f1.read() #reads the entire file
                #print(description)

            category = '25'
            #tags is a string, which when put into the json file, will appear as a list
            tags = f'["news","1","one","minute","one minute","headline","{date}","{country[0]}"]'
            privacy = 'private' #change to 'public' later

            #need to create a json file to put in the metadata
            #i need \\ in the discription's \n
            #the double \\ is to tell python that iwant to wqrite it out as \n in the json document
            #need to do this cause multyiline not supported in json
            with open(f'{country[0]}_{date}.json', 'w', encoding='utf-8') as f2:
                f2.write('{\n')
                f2.write(f'"title": "{title}",\n')
                #f2.write(f"'category': '{category}',\n")
                f2.write(f'"description": "{description}",\n')
                f2.write(f'"tags": {tags}\n')
                #f2.write(f"'privacy': '{privacy}',\n")
                f2.write('}')
                        
            metadata_path = f'{country[0]}_{date}.json'

            uploader = YouTubeUploader(filepath, metadata_path)#, thumbnail_path)
            uploader.upload()
    ####        was_video_uploaded, video_id = uploader.upload()
    ####        assert was_video_uploaded

            ##Move all the files fro the root folderinto its correct date folder
            #i put after everything is done to prevent it from crashing the program
            for file in os.listdir():
                if date in file and country[0] in file and '.json' in file:
                    try:
                        shutil.move(file, f'{date}')
                    except Exception as e:
                        print(e)
                        
