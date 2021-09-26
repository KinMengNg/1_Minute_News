#for firefox
from selenium_firefox.firefox import Firefox
import time
from pathlib import Path

current_working_dir = str(Path.cwd())
driver = Firefox(current_working_dir,current_working_dir)#, user_agent = 'random')
driver.get('https://www.youtube.com')
time.sleep(1)

#to load my profile basically
if driver.has_cookies_for_current_website():
    driver.load_cookies()
    time.sleep(1)
    driver.refresh()

input('press ENTER when i have done everything i want to, to save new cookies and close window')
driver.save_cookies()
driver.driver.quit()
