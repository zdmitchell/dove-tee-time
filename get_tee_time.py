from selenium import webdriver
import json

fname = 'settings.json'

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
