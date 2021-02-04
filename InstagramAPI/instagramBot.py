from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import urllib.request
import time
import sys

timer = 10 #seconds
username = "mulez123456@gmail.com"
password = "SandeepFan"
counter = 0

while True:
    try:
        print ("Loading page...")
        urllib.request.urlopen("https://www.instagram.com/")
    except:
        counter += 1
        if counter > 10:
            print ("Page didn't load after 10 attempts... shutting down...")
            sys.exit(0)

        print ("Some error occured loading page... retrying in {}s...". format(timer))
        time.sleep(timer)
        continue

    #keep trying until loaded
    break

PATH = "C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(timer)
driver.get("https://www.instagram.com/")

while True:
    try:
        print ("Entering username...")
        search = driver.find_element_by_name("username")
        search.send_keys(username)
    except NoSuchElementException:
        counter += timer
        print ('Username Box failed to load after {0}s... retrying...'.format(counter))
        continue

    #keep retrying until no exception
    break

counter = 0

while True:
    try:
        print ("Entering password...")
        search = driver.find_element_by_name("password")
        search.send_keys(password)
    except NoSuchElementException:
        counter += timer
        print ('Password Box failed to load after {0}s... retrying...'.format(counter))
        continue

    #keep retrying until no exception
    break


#enter login info
search.send_keys(Keys.RETURN)

time.sleep(10)