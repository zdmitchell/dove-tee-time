from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import date, time, datetime
from calendar import month_name
import sys

def main():
   fname = 'settings.json'
   delay = 10 # seconds max wait

   try:
      settings_file = open(fname)
   except FileNotFoundError:
      print("File %s not found" % fname)
      exit()

   with settings_file:
      settings = json.load(settings_file)

   today = date.today()

   day_to_book = date(today.year, settings['month'], settings['day'])
   earliest_time = datetime.strptime(settings['earliestTime'], '%I:%M %p').time()

   browser = webdriver.Firefox()
   browser.get("https://web.foretees.com/v5/servlet/LoginPrompt?cn=dovecanyonclub")

   browser.find_element_by_id('user_name').send_keys(settings['username'])
   browser.find_element_by_id('password').send_keys(settings['password'])
   browser.find_element_by_css_selector('#login input[type="submit"]').submit()

   WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'topnav_item')))
   browser.get("https://web.foretees.com/v5/dovecanyonclub_golf_m0/Member_select")

   calendar_months = browser.find_elements_by_class_name('ui-datepicker-inline')

   for month in calendar_months:
      title = month.find_element_by_class_name('ui-datepicker-title')

      if title.find_element_by_class_name('ui-datepicker-month').get_attribute("textContent") == month_name[day_to_book.month]:
         month_to_find = month
         break

   try:
      month_to_find
   except NameError:
      print("Can't book tee time for month you specified")
      exit()

   selectable_days = month.find_elements_by_css_selector('tbody a.ui-state-default')

   for calendar_day in selectable_days:
      if int(calendar_day.get_attribute("textContent")) == day_to_book.day:
         day_link = calendar_day
         break

   try:
      day_link
   except NameError:
      print("Cannot make tee times for the day you specified")
      exit()

   day_link.click()

   tee_time_rows = browser.find_elements_by_css_selector('table.member_sheet_table tbody tr')

   for tee_time_row in tee_time_rows:
      try:
         tee_time_link = tee_time_row.find_element_by_css_selector('a.teetime_button')
      except NoSuchElementException:
         continue

      tee_time_text = tee_time_link.get_attribute("textContent")
      tee_time = datetime.strptime(tee_time_text, '%I:%M %p').time()

      if tee_time >= earliest_time and count_open_spots(tee_time_row) >= len(settings['otherPlayers']) + 1:
         tee_time_link.click()
         break

   WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.partner_list option')))

   otherPlayers = settings['otherPlayers']

   for player in otherPlayers:
      name = player['firstName'] + ' ' + player['lastName']

      try:
         player_item = browser.find_element_by_css_selector('option[value="%s"' % name)
      except NoSuchElementException:
         print("Player %s is not in your Name List" % name)
      else:
         player_item.click()

   player_rows = browser.find_elements_by_css_selector('.request_container tr.slot_player_row')

   for player_row in player_rows:
      nineHolesCheckbox = player_row.find_element_by_css_selector('input.slot_9holes')

      if not nineHolesCheckbox.get_attribute('disabled'):
         nineHolesCheckbox.click()

   if '-d' in sys.argv or 'debug' in sys.argv:
      exit()

   browser.find_element_by_css_selector('.request_container .submit_request_button').click()

   browser.close()

def count_open_spots(tee_time_row):
   open_spots = 0
   player_slots = tee_time_row.find_elements_by_css_selector('td.sP')

   for player_slot in player_slots:
      if player_slot.get_attribute("textContent") == "":
         open_spots = open_spots + 1

   return open_spots

if __name__ == '__main__':
   main()
