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
from Variables import workbookNameData
# -*- coding: utf-8 -*-


def AdjustResolution():
    display = Display(visible=0, size=(800, 800))
    display.start()


workbook = xlrd.open_workbook(workbookNameData)
worksheet = workbook.sheet_by_index(0)
url = worksheet.cell(1, 0).value
username = worksheet.cell(1, 1).value
password = worksheet.cell(1, 2).value
adjustResolution = worksheet.cell(1, 3).value


if adjustResolution == 1:
    AdjustResolution()


def delete_place(placeID, authToken):
    headers = {'host': 'hb.511.nebraska.gov'}
    deleteUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/3763/trips/' + str(placeID) + '?authTokenId=' + str(authToken)
    deleteItem = requests.delete(deleteUrl, headers=headers)
    # print deleteItem.status_code


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
    customAreasAPIUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(
        accountID) + '/trips?authTokenId=' + str(authToken)
    customAreaJson = requests.get(customAreasAPIUrl, headers=headers)
    data = customAreaJson.json()
    indexNumber = 0
    if len(data) > 0:
        for x in data:
            routeID = data[indexNumber].get('id')
            delete_place(routeID, authToken)
            indexNumber += 1


class Verify_Login_And_Saving_Routes(unittest.TestCase):


    def setUp(self):
        # Includes options for the ModHeader chrome extension
        options = webdriver.ChromeOptions()
        options.add_extension('ModHeader_v2.1.2.crx')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.maximize_window()


    def test_login_route_creation_and_deletion(self):
        driver = self.driver

        #   RUN SCRIPT FOR HEADERS
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

        #   HEAD TO WEBSITE
        driver.get(url)

        #   SELECT THE FAVORITE PAGE
        pageLoadWait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'favoriteBtn')))
        time.sleep(2)
        signInButton = driver.find_element_by_id('favoriteBtn')
        signInButton.click()

        #   LOGIN INFO/LOGIN BUTTON
        pageLoadWait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'userAccountEmail')))
        driver.find_element_by_id('userAccountEmail').send_keys(username) # Login
        driver.find_element_by_id('userAccountPassword').send_keys(password)
        driver.find_element_by_id('userAccountPassword').submit()

        #   HEAD TO THE SEARCH PAGE
        pageLoadWait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'searchBtn')))
        searchButton = driver.find_element_by_id('searchBtn')
        clickLoadWait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'searchBtn')))
        time.sleep(2)
        searchButton.click()

        #  ENTER LOCATIONS A & B
        time.sleep(2)
        driver.find_element_by_id('address0').send_keys('Columbus, NE, United States')
        time.sleep(2)
        driver.find_element_by_id('address0').send_keys(Keys.RETURN)
        driver.find_element_by_id('address1').send_keys('Hastings, NE, United States')
        time.sleep(2)
        driver.find_element_by_id('address1').send_keys(Keys.RETURN)
        time.sleep(2)
        driver.find_element_by_id('pickARouteSearchBtn').click()

        #  SAVE THE LINK
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="leftPanelContent"]/div/div[3]/a').click() # Clicking the save this link

        #  CLICK SUBMIT
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="save-route-form"]/button').submit() # Clicking the submit button

        #   ASSERT THE SAVE FUNCTION WORKED AND WE ARE NOW ON THE 'FAVORITES' PAGE
        pageLoadWait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "favorites-content-area")))
        assert (driver.find_element_by_id("favorites-content-area").is_displayed()), 'Event Edits Creation Button Is Not Displayed' # Did we make it to the 'Favorites' page

        #   DELETE IT ALL
        get_authToken_and_call_delete_function()


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
