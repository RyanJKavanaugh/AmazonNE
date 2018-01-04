# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import unittest
import json
import requests
import xlrd
from pyvirtualdisplay import Display
from Variables import NEWPLACEJSON1, NEWPLACEJSON2, NEWPLACEJSON3
# -*- coding: utf-8 -*-


class CONSTANTS:
    URL = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/#favorites?layers=roadReports%2Ccameras&timeFrame=TODAY'

    PLACESJSON = []
    PLACESJSON.append(NEWPLACEJSON1)
    PLACESJSON.append(NEWPLACEJSON2)
    PLACESJSON.append(NEWPLACEJSON3)


def get_permissions_data(headers):
    userInfo = {"userId": "ryan.kavanaugh@crc-corp.com", "password": "test"}
    authTokenURL = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/authTokens'
    myResponse = requests.post(authTokenURL, json=userInfo, headers=headers)
    jData = json.loads(myResponse.content)
    return jData


def get_currently_saved_places(headers, accountID, authToken):
    customAreasAPIUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(accountID) + '/customAreas?authTokenId=' + str(authToken)
    customAreaJson = requests.get(customAreasAPIUrl, headers=headers)
    data = customAreaJson.json()
    if len(data) > 0:
        print 'The following places are saved for this user:'
        printCounter = 0
        while printCounter < len(data):
            print printCounter + 1
            print data[printCounter].get('name')
            printCounter += 1


def post_new_places(placesJson, authToken, headers, accountID):
    listOfIDs = []
    for item in placesJson:
        apiUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(accountID) + '/customAreas?authTokenId=' + str(authToken)
        newPlacePost = requests.post(apiUrl, json=item, headers=headers)
        data = json.loads(newPlacePost.content)
        id = data.get('id')
        listOfIDs.append(id)
    return listOfIDs


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


def login_and_head_to_favorites_page(driver):
    # Open browser and login
    driver.get(CONSTANTS.URL)
    loginElement = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'userAccountEmail')))
    driver.find_element_by_id('userAccountEmail').send_keys('ryan.kavanaugh@crc-corp.com')
    driver.find_element_by_id('userAccountPassword').send_keys('test')
    driver.find_element_by_id('userAccountPassword').submit()

    # Head to the favorites page
    pageLoadWait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'favoriteBtn')))
    time.sleep(2)
    signInButton = driver.find_element_by_id('favoriteBtn')
    signInButton.click()


def assert_the_correct_places_are_saved_to_TG_Web(driver):
    favoritesPageWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'user-favorite-item')))
    allFavoritesPlaces = driver.find_elements_by_class_name('user-favorite-item')

    BrokenBow = False
    Elmwood = False
    Callaway = False

    for favorite in allFavoritesPlaces:
        # print favorite.text
        favoritesWithAPIInfo = favorite.text
        if 'Broken Bow' in favoritesWithAPIInfo:
            BrokenBow = True
        if 'Elmwood' in favoritesWithAPIInfo:
            Elmwood = True
        if 'Callaway' in favoritesWithAPIInfo:
            Callaway = True

    # Assert that the places we created showed up in the list of favorites saved to the TG Web app
    assert BrokenBow
    assert Elmwood
    assert Callaway


def delete_places(placeIDs, authToken, headers, accountID):
    for placeID in placeIDs:
        deleteUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(
            accountID) + '/customAreas/' + str(placeID) + '?authTokenId=' + str(authToken)
        deleteItem = requests.delete(deleteUrl, headers=headers)


class Verify_Saved_Places_Via_The_API(unittest.TestCase):


    def test_create_new_places(self):
        headers = {'host': 'hb.511.nebraska.gov'}

        # Gather permissions data for working with the API
        permissionsData = get_permissions_data(headers)
        authToken = permissionsData.get('id')
        accountID = permissionsData.get('accountId')

        # Gather and print currently saved places for testing purposes
        get_currently_saved_places(headers, accountID, authToken)

        # Create new places and return their unique IDs
        placeIDs = post_new_places(CONSTANTS.PLACESJSON, authToken, headers, accountID)

        # Verify new places are saved in TG Web
        driver = amz_headers_and_return_driver()
        login_and_head_to_favorites_page(driver)
        assert_the_correct_places_are_saved_to_TG_Web(driver)

        #   API clean up
        delete_places(placeIDs, authToken, headers, accountID)


if __name__ == '__main__':
    unittest.main()