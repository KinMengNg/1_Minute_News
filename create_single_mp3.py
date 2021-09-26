#to create a single mp3 for whatever reason i want

import pyttsx3

def saveToFile(audio, title):
    print(audio)
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    engine.setProperty('rate', 130)     # setting up new voice rate

    name = f'{title}.mp3'
    #path = f'/{date}/{name}'
    engine.save_to_file(audio, name)
    engine.runAndWait()

saveToFile('The links to these headlines are in the description below. . . See you again tomorrow!\n', 'outtro_extended')
