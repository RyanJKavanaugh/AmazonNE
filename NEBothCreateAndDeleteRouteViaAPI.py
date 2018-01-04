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
from Variables import WORKBOOKNAMEDATA, CREATEROUTEJSON
# -*- coding: utf-8 -*-

# Function allowing Google Chrome to run on a virtual Jenkins server by providing a virtual window
def AdjustResolution():
    display = Display(visible=0, size=(800, 800))
    display.start()

class Constants:
    WORKBOOK = xlrd.open_workbook(WORKBOOKNAMEDATA)
    WORKSHEET = WORKBOOK.sheet_by_index(0)
    URL = WORKSHEET.cell(1, 0).value
    USERNAME = WORKSHEET.cell(1, 1).value
    PASSWORD = WORKSHEET.cell(1, 2).value
    ADJUSTRESOLUTION = WORKSHEET.cell(1, 3).value


if Constants.ADJUSTRESOLUTION == 1:
    AdjustResolution()


def post_place_to_api(placeJson, authToken, accountID, headers):
    apiPostUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(accountID) + '/trips?authTokenId=' + str(authToken)
    newPlacePost = requests.post(apiPostUrl, json=placeJson, headers=headers)


def delete_place(placeID, authToken, accountID):
    headers = {'host': 'hb.511.nebraska.gov'}
    deleteUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(accountID) + '/trips/' + str(placeID) + '?authTokenId=' + str(authToken)
    deleteItem = requests.delete(deleteUrl, headers=headers)


def get_authToken_and_call_delete_function():
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


class Verify_Login_And_Saving_Routes_Via_API(unittest.TestCase):


    def setUp(self):
        # Includes options for the ModHeader chrome extension
        options = webdriver.ChromeOptions()
        options.add_extension('ModHeader_v2.1.2.crx')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.maximize_window()


    def test_login_route_creation_and_deletion(self):
        userInfo = {"userId": "ryan.kavanaugh@crc-corp.com", "password": "test"}
        authTokenURL = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/authTokens'
        headers = {'host': 'hb.511.nebraska.gov'}

        myResponse = requests.post(authTokenURL, json=userInfo, headers=headers)
        jData = json.loads(myResponse.content)
        authToken = jData.get('id')
        accountID = jData.get('accountId')

        post_place_to_api(CREATEROUTEJSON, authToken, accountID, headers)

        driver = self.driver
        # RUN SCRIPT FOR HEADERS
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

        # HEAD TO WEBSITE
        driver.get(Constants.URL)

        # Wait time variable
        waitTime = WebDriverWait(driver, 30)

        # SELECT THE FAVORITE PAGE
        pageLoadWait = waitTime.until(EC.element_to_be_clickable((By.ID, 'favoriteBtn')))
        time.sleep(2)
        signInButton = driver.find_element_by_id('favoriteBtn')
        signInButton.click()

        # LOGIN INFO/LOGIN BUTTON
        pageLoadWait = waitTime.until(EC.element_to_be_clickable((By.ID, 'userAccountEmail')))
        driver.find_element_by_id('userAccountEmail').send_keys(Constants.USERNAME) # Login
        driver.find_element_by_id('userAccountPassword').send_keys(Constants.PASSWORD)
        driver.find_element_by_id('userAccountPassword').submit()

        # HEAD TO THE FAVORITES PAGE
        time.sleep(2)
        driver.find_element_by_id('favoriteBtn').click() # Clicking the save this link

        # NAVIGATE TO THE 'FAVORITES' PAGE
        pageLoadWait = waitTime.until(EC.presence_of_element_located((By.ID, "favorites-content-area")))

        # ASSERT THE ROUTE WAS CREATED IN TG WEB
        elementLoadWait = waitTime.until(EC.presence_of_element_located((By.CLASS_NAME, "showRoute")))
        usersFavoriteRoutes = driver.find_elements_by_class_name('showRoute')

        testPasses = False

        for route in usersFavoriteRoutes:
            if 'Henderson to Minden' in route.text:
                testPasses = True

        assert testPasses

        #   DELETE ALL ROUTES
        get_authToken_and_call_delete_function()


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()