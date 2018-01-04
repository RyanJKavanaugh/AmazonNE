# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests
import time
import unittest
import xlrd
import json
from pyvirtualdisplay import Display
from Variables import WORKBOOKNAMEDATA
# -*- coding: utf-8 -*-


def AdjustResolution():
    # Function that allows Google Chrome to run on a virtual Jenkins server by providing a virtual window
    display = Display(visible=0, size=(800, 800))
    display.start()

class CONSTANTS:
    WORKBOOK = xlrd.open_workbook(WORKBOOKNAMEDATA)
    WORKSHEET = WORKBOOK.sheet_by_index(0)
    URL = WORKSHEET.cell(1, 0).value
    USERNAME = WORKSHEET.cell(1, 1).value
    PASSWORD = WORKSHEET.cell(1, 2).value
    ADJUSTRESOLUTION = WORKSHEET.cell(1, 3).value


if CONSTANTS.ADJUSTRESOLUTION == 1:
    AdjustResolution()


def amz_headers_and_return_driver():
    options = webdriver.ChromeOptions()
    options.add_extension('ModHeader_v2.1.2.crx')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get("chrome-extension://idgpnmonknjnojddfkpgkljpfnnfcklj/icon.png")
    driver.execute_script(
        "localStorage.setItem('profiles', JSON.stringify([{                " +
        "  title: 'Selenium', hideComment: true, appendMode: '',           " +
        "  headers: [                                                      " +
        "    {enabled: true, name: 'Host', value: 'hb.511.nebraska.gov', comment: ''}, " +
        "  ],                                                              " +
        "  respHeaders: [],                                                " +
        "  filters: [{enabled: true, type: 'urls', urlPattern : '*//*crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/*' , comment: ''},]                                                     " +
        "}]));")
    return driver


def login_and_navigate_to_the_search_page(driver, waitTime):
    # Navigate to the favorites page
    pageLoadWait = waitTime.until(EC.element_to_be_clickable((By.ID, 'favoriteBtn')))
    time.sleep(2)
    signInButton = driver.find_element_by_id('favoriteBtn')
    signInButton.click()

    # Login
    pageLoadWait = waitTime.until(EC.element_to_be_clickable((By.ID, 'userAccountEmail')))
    driver.find_element_by_id('userAccountEmail').send_keys(CONSTANTS.USERNAME)  # Login
    driver.find_element_by_id('userAccountPassword').send_keys(CONSTANTS.PASSWORD)
    driver.find_element_by_id('userAccountPassword').submit()

    # Head to the search page
    pageLoadWait = waitTime.until(EC.presence_of_element_located((By.ID, 'searchBtn')))
    searchButton = driver.find_element_by_id('searchBtn')
    clickLoadWait = waitTime.until(EC.element_to_be_clickable((By.ID, 'searchBtn')))
    time.sleep(2)
    searchButton.click()


def delete_place(placeID, authToken, accountID):
    headers = {'host': 'hb.511.nebraska.gov'}
    deleteUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(accountID) + '/trips/' + str(placeID) + '?authTokenId=' + str(authToken)
    deleteItem = requests.delete(deleteUrl, headers=headers)


def delete_all_routes_function():
    #   Variables
    userInfo = {"userId": "ryan.kavanaugh@crc-corp.com", "password": "test"}
    authTokenURL = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/authTokens'
    headers = {'host': 'hb.511.nebraska.gov'}

    myResponse = requests.post(authTokenURL, json=userInfo, headers=headers)
    jData = json.loads(myResponse.content)
    authToken = jData.get('id')
    accountID = jData.get('accountId')

    #   Get all saved routes and delete the routes
    customAreasAPIUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(accountID) + '/trips?authTokenId=' + str(authToken)
    customAreaJson = requests.get(customAreasAPIUrl, headers=headers)
    data = customAreaJson.json()
    indexNumber = 0
    if len(data) > 0:
        for x in data:
            routeID = data[indexNumber].get('id')
            delete_place(routeID, authToken, accountID)
            indexNumber += 1


def create_and_verify_route(driver, waitTime):
    # Enter two locations for a saved route
    driver.find_element_by_id('address0').send_keys('Columbus, NE, United States')
    time.sleep(2)
    driver.find_element_by_id('address0').send_keys(Keys.RETURN)
    driver.find_element_by_id('address1').send_keys('Hastings, NE, United States')
    time.sleep(2)
    driver.find_element_by_id('address1').send_keys(Keys.RETURN)
    time.sleep(2)
    driver.find_element_by_id('pickARouteSearchBtn').click()

    # Save the link
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="leftPanelContent"]/div/div[3]/a').click()  # Clicking the save this link

    # Click submit
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="save-route-form"]/button').submit()  # Clicking the submit button

    # Assert the route was saved correctly to the TG Web page
    pageLoadWait = waitTime.until(EC.presence_of_element_located((By.ID, "favorites-content-area")))
    assert (driver.find_element_by_id("favorites-content-area").is_displayed()), 'Event Edits Creation Button Is Not Displayed'  # Did we make it to the 'Favorites' page



class Verify_Login_And_Saving_Routes(unittest.TestCase):


    def test_login_route_creation_and_deletion(self):

        # Take care of the amazon headers required at this stage and return a webdriver instance
        driver = amz_headers_and_return_driver()

        # Head to the agency TG Web site
        driver.get(CONSTANTS.URL)

        # Wait time variable
        waitTime = WebDriverWait(driver, 30)

        # Login and head to the page used for creating routes
        login_and_navigate_to_the_search_page(driver, waitTime)

        # create the route and assert it is saved to TG Web
        create_and_verify_route(driver, waitTime)

        # Delete all of the saved routes to clean up
        delete_all_routes_function()


if __name__ == '__main__':
    unittest.main()
