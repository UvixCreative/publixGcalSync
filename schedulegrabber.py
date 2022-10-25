#!/bin/python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from os import path

import time
import datetime
import re
import array

import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/calendar']


if path.exists('./passwd') and path.exists('./username'):
    #Log in to google calendar
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/ben/Sync/code/calendar-credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    gcal = build('calendar', 'v3', credentials=creds)

    #grab the password from the password file
    loginpass = open('./passwd',mode='rt').read()
    username = open('./username',mode='rt').read()
    
    #open the login page
    driver = webdriver.Firefox()
    driver.get('https://oasis-sso.publix.org/ess/portal?siteId=0866#wfmess/wfmess-myschedule////')
    
    #login
    ae = driver.find_element_by_id('userNameInput')
    ae.send_keys(username)
    ae = driver.find_element_by_id('passwordInput')
    ae.send_keys(loginpass)
    ae = driver.find_element_by_id('submitButton')
    ae.click()

    #wait for the schedule to load, enter the iframe
    ##Should eventually have a condition to check when the page is loaded rather than just waiting
    time.sleep(10)
    driver.switch_to.frame(driver.find_element_by_id('jdaIFrame-1023'))
    #Navigate to whatever "next week" is
    comp = False
    while comp == False:
        selweek_el = driver.find_element_by_id('textfield-1026-inputEl')
        selweek = selweek_el.get_attribute('value')
        x = re.split(" - ",selweek)
        today = datetime.datetime.today()
        weekstart = datetime.datetime.strptime(x[0], '%m/%d/%Y')
        comp = True
        comp = today < weekstart
        if comp == False:
            ae = driver.find_element_by_id('button-1029')
            ae.click()
            time.sleep(3)
    #Define the dates of the work week. -1 is a placeholder so that workweek[1] is the first day of the week. This is mostly because in shifttimes, the first object is "schedule hours"
    #which means that shifttimes[1] is actually the first shift
    workweek = ['-1']
    for x in range(0, 7):
        day = weekstart + datetime.timedelta(days=x)
        workweek.append(day.date())

    #Find the shifts from within the grid, break apart the info, turn it into datetime
    col_el = driver.find_elements_by_css_selector('div.x-grid-cell-inner')
    col = [x.text for x in col_el]
    shiftstr = []
    for x in range(0, len(col)):
        shiftstr.append(re.split("\n| - |M:",col[x]))

    #Test the parsed information. Soon will actually make shifts[] where shifts[0][0] through shifts[6][4] define the entire shift 
    for x in range(1,8):
        curday = workweek[x].strftime('%Y-%m-%d')
        if len(shiftstr[x]) > 1:
            shiftstarttime = datetime.datetime.strptime(shiftstr[x][0],'%I:%M %p').time()
            shiftendtime = datetime.datetime.strptime(shiftstr[x][1],'%I:%M %p').time()
            shiftstart = curday+"T"+shiftstarttime.strftime('%H:%M:00')+"-04:00"
            shiftend = curday+"T"+shiftendtime.strftime('%H:%M:00')+"-04:00"
            event = {
                'summary': 'Work',
                'start': {
                    'dateTime': shiftstart,
                    'timeZone': 'America/New_York',
                },
                'end': {
                    'dateTime': shiftend,
                    'timeZone': 'America/New_York',
                },
                'reminders': {
                    'useDefault': True,
                },
            }
            event = gcal.events().insert(calendarId='r4uvp9udl61ma31emvhungml1g@group.calendar.google.com', body=event).execute()
    
    print("Done!")
    driver.quit()
else:
    print("ERROR: No password or username set")
