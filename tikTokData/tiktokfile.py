"""
Use this program to sift thru my entire TikTok Browsing history
Had a video stuck in my head and I couldn't find it in my saved videos
Version: Spring 2021
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 

timer = 10 #seconds

PATH = "C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(timer)
driver.get("https://www.google.com/")

def main():
    file_object = open("Video Browsing History.txt", "r")
    
    counter = 0
    while True:
        if counter < 2030:
            counter += 1
            line = file_object.readline()
            print (counter)
            continue
        
        line = file_object.readline()

        if (counter % 3 == 1):
            line = line.removeprefix("Video Link: ")
            print (counter, "\t", line)
            # body = driver.find_element_by_tag_name("body")
            # body.send_keys(Keys.CONTROL + 't')
            driver.get(line)
            
            # print (line)

        counter += 1
        


if __name__ == "__main__":
    main()