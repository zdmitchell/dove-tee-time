from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

fname = 'settings.json'
delay = 10 # seconds max wait

try:
   settings_file = open(fname)
except FileNotFoundError:
   print("File %s not found" % fname)
   exit()

with settings_file:
   settings = json.load(settings_file)

browser = webdriver.Firefox()
browser.get("https://web.foretees.com/v5/servlet/LoginPrompt?cn=dovecanyonclub")

browser.find_element_by_id('user_name').send_keys(settings['username'])
browser.find_element_by_id('password').send_keys(settings['password'])
browser.find_element_by_css_selector('#login input[type="submit"]').submit()


WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'topnav_item')))
browser.get("https://web.foretees.com/v5/dovecanyonclub_golf_m0/Member_select")
