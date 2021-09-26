#i run this after getting my audio files
#How i am creating the video is by
#1.create the video without the audio, just according to its necesarry duration based on the audio files
#2.then using the soundless created video, add the audio filesinto the correct placesa




##############################################~
'''
#DO NOT RUN FROM IDLE
#RUN FROM POWERSHELL OR CMD, cause its very slow in idle due to the printing progress bar
#USE:
#python video_creator.py
'''
#####################################################
import datetime
import os
from moviepy.editor import *
import shutil
from inputimeout import inputimeout, TimeoutOccurred

#All country codes: https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes
country_codes = [('Singapore','SG'), ('Malaysia','MY'), ('United States','US'), ('United Kingdom','UK'), ('India','IN'), ('Australia','AU'), ('New Zealand', 'NZ'), ('South Africa', 'ZA'), ('Indonesia', 'ID')]

date = str(datetime.date.today()) #todays date, is my path to folder too

#im creating one video for each country
for country in country_codes:
    prompt = ''
    
    while prompt != 'y' and prompt != 'n':
        #without timeout
        #prompt = input(f'Would you like to create video for {country[0]} ? [Y/N]')
        #with timeout
        try:
            prompt = inputimeout(prompt=f'Would you like to create video for {country[0]} ? [y/n]: ', timeout=5)
        except TimeoutOccurred:
            print('Timed Out! Defaulting to Yes.')
            prompt = 'y'


    if prompt.lower() == 'y':
        #check if its already been done, if it has, skip
        if os.path.exists(f'{date}/videos/{country[0]}_{date}_video.mp4'):
            continue
        else:
            print(f'Starting with {country[0]}')
            video_name = f'{country[0]}_{date}_video.mp4'
            clips = [] #empty list that i will eventually put all my clips in and make the video
            #each clip is an object that i can add audio and stuff to it
            
            #make the intro
            for file in os.listdir(f'Intros'):
                #only 1 file in this directory sdhould have the country name
                if country[0] in file:
                    audio = AudioFileClip(f'Intros/{file}')
                    clip = ImageClip('Intros/black_screen.png').set_duration(audio.duration)
                    clip = clip.set_audio(audio)
                    clips.append(clip)
                    
            #the content
            for file in os.listdir(f'{date}'):
                if country[0] in file and '.mp3' in file:#to make sure no duplication
                    audio = AudioFileClip(f'{date}/{file}')
                    clip = ImageClip(f'{date}/{file[:-4]}.png').set_duration(audio.duration)
                    clip = clip.set_audio(audio)
                    clips.append(clip)

            #the outtro
            audio = AudioFileClip('outtro_extended.mp3')
            clip = ImageClip('Intros/black_screen.png').set_duration(audio.duration)
            clip = clip.set_audio(audio)
            clips.append(clip)


            #make the video
            concat_clip = concatenate_videoclips(clips, method="compose")
            concat_clip.write_videofile(video_name, threads=8, fps=24) #progress_bar = False

            ##Move all the files from the root folderinto its correct date folder
            for file in os.listdir():
                if date in file and 'video' in file:
                    shutil.move(file, f'{date}/videos')
            
        
    
    
