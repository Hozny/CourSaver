###############################################################################
###                                CourSaver                                ###
###       A script to download all course content from UW Learn courses.    ###
###  ---------------------------------------------------------------------  ###
### Usage: run the script in a directory with courses.txt which must        ###
###        contain the Learn links to the homepage of courses you would     ###
###        like to download. Zipped folders for each course should          ###
###        eventually be found in your downloads directory                  ###
### Note: if pages are loading too slow (causing timeout exceptions)        ###
###       increase delay                                                    ###
###############################################################################

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

import time

# File should contain Learn course links (one per line)
courses = open("courses.txt", "r")

userName = input("Enter username (e.g userid@uwaterloo.ca): ")
userPass = input("Enter your password: ")

print("Select one of the following for two factor authentication")
print("\tEnter (1) for Duo Push")
print("\tEnter (2) for Call Me")
twoFacAuthChoice = input(">") 
while (twoFacAuthChoice != '1' and twoFacAuthChoice != '2'): 
    print("Invalid choice")
    print("\tEnter (1) for Duo Push")
    print("\tEnter (2) for Call Me")
    twoFacAuthChoice = input(">") 
twoFacAuthChoice = int(twoFacAuthChoice)

# Change delay time to wait for each page to load (increase if pages load too slow for script)
delay = 5

driver = webdriver.Chrome()
driver.get('https://learn.uwaterloo.ca/d2l/home')

# Enter username and continue
username_textbox = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'userNameInput')))
username_textbox.send_keys(userName)
next_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'nextButton')))
next_button.submit()

# Enter password and continue
password_textbox = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'passwordInput')))
password_textbox.send_keys(userPass)
submit_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'submitButton')))
submit_button.submit()

# Switch to Duo's iframe
iframe = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'duo_iframe')))
driver.switch_to.frame(iframe)

if (twoFacAuthChoice == 1): 
    authChoice_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="auth_methods"]/fieldset/div[1]/button')))
else: 
    authChoice_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="auth_methods"]/fieldset/div[2]/button')))
authChoice_button.click()

# Force wait until authentication is complete
while (driver.current_url != 'https://learn.uwaterloo.ca/d2l/home'):
    time.sleep(1)

courseLinks = []
for line in courses: 
    if (len(line) > 0): 
        courseLinks.append(str(line).rstrip())

for course in courseLinks: 
    print(course)
    driver.execute_script('''window.open("{0}","_blank");'''.format(course))
    driver.switch_to.window(driver.window_handles[-1])

    while (driver.current_url != course):
        time.sleep(1)

    contentButton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/header/nav/d2l-navigation/d2l-navigation-main-footer/div/div/div[2]/a')))
    contentButton.click()

    tableOfContentsButton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="TreeItemTOC"]/div[1]')))
    tableOfContentsButton.click()

    # force wait for download button to load in 
    for wait in range(delay):
        time.sleep(1)

    downloadButton = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div/div[4]/button')))
    downloadButton.click()

    time.sleep(1)

driver.close()

