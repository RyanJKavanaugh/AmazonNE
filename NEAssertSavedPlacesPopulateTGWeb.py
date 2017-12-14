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
# -*- coding: utf-8 -*-

# /Users/ryankavanaugh/Desktop/AmazonNE/

def post_new_place(placeJson, authToken):
    apiUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/3757/customAreas?authTokenId=' + str(authToken)
    newPlacePost = requests.post(apiUrl, json=placeJson)

    data = json.loads(newPlacePost.content)
    id = data.get('id')
    return id


def delete_place(placeID, authToken):
    deleteUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/3757/customAreas/' + str(placeID) + '?authTokenId=' + str(authToken)
    deleteItem = requests.delete(deleteUrl)
    print deleteItem.status_code


class Verify_Saved_Places_Via_The_API(unittest.TestCase):


    def test_login(self):

        #   VARIABLES
        userInfo = {"userId":"ryan.kavanaugh@crc-corp.com","password":"test"}
        authTokenURL = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/authTokens'

        headers = {'host': 'hb.511.nebraska.gov'}

        # Json for different places for testing saved 'favorite places'
        newPlace = {"accountId":2309,"name":"Carmel, IN, United States","normalDuration":None,"polygon":{"type":"Polygon","coordinates":[[[-86.48051327246094,39.77217256505626],[-86.48051327246094,40.15425322804566],[-85.78425472753906,40.15425322804566],[-85.78425472753906,39.77217256505626],[-86.48051327246094,39.77217256505626]]]},"bounds":None,"customAreaShapeSource":"CONFIG_DEFINED","embedded":{},"id":None}
        #newPlace2 = {"accountId":15466,"name":"Louisiana","normalDuration":None,"polygon":{"type":"Polygon","coordinates":[[[-107.364004765625,27.5582840804247],[-107.364004765625,34.244808909713534],[-75.437735234375,34.244808909713534],[-75.437735234375,27.5582840804247],[-107.364004765625,27.5582840804247]]]},"bounds":None,"customAreaShapeSource":"CONFIG_DEFINED","embedded":{},"id":None}
        #newPlace3 = {"accountId":15466,"name":"Baton Rouge","normalDuration":None,"polygon":{"type":"Polygon","coordinates":[[[-92.21211129902338,30.231198967440722],[-92.21211129902338,30.651510408818112],[-90.0107258009765,30.651510408818112],[-90.0107258009765,30.231198967440722],[-92.21211129902338,30.231198967440722]]]},"bounds":None,"customAreaShapeSource":"CONFIG_DEFINED","embedded":{},"id":None}


        myResponse = requests.post(authTokenURL, json=userInfo, headers=headers)
        jData = json.loads(myResponse.content)
        authToken = jData.get('id')
        accountID = jData.get('accountId')





        #   GET INITIAL SAVED PLACES VIA API (do I really need this ??? )
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 777 Gets the user's current saved places and prints them out:
        customAreasAPIUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(accountID) + '/trips?authTokenId=' + str(authToken)
        customAreaJson = requests.get(customAreasAPIUrl, headers=headers)
        print customAreaJson.status_code
        data = customAreaJson.json()

        print

        print 'ID 1'
        print data[0]['id']

        print 'ID 2'
        print data[1]['id']

        print

        if len(data) > 0:
            print 'There are still events here'
            printCounter = 0
            while printCounter < len(data):
                print printCounter
                print data[printCounter].get('name')
                printCounter+=1
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



        #   CREATE PLACES VIA API
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Calls above function to post new place to the API and ultimately TG Web
        # id1 = post_new_place(newPlace, authToken)
        # id2 = post_new_place(newPlace2, authToken)
        # id3 = post_new_place(newPlace3, authToken)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        #   SELENIUM WEBDRIVER IN TG WEB
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Selenium Verification (that the places appear in TG WEB)
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
            "}]));                                                             ")

        url = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/#favorites?layers=roadReports%2Ccameras&timeFrame=TODAY'

        driver.get(url)
        loginElement = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'userAccountEmail')))
        driver.find_element_by_id('userAccountEmail').send_keys('ryan.kavanaugh@crc-corp.com')
        driver.find_element_by_id('userAccountPassword').send_keys('test')
        driver.find_element_by_id('userAccountPassword').submit()

        # Head to the favorites page
        pageLoadWait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'favoriteBtn')))
        time.sleep(2)
        signInButton = driver.find_element_by_id('favoriteBtn')
        signInButton.click()

        time.sleep(6)
        allFavoritesPlaces = driver.find_elements_by_class_name('user-favorite-item')

        Elton = False
        Lou = False
        BatonRouge = False

        for favorite in allFavoritesPlaces:
            print favorite.text
            favoritesWithAPIInfo = favorite.text
            if 'Elton' in favoritesWithAPIInfo:
                Elton = True
            if 'Louisiana' in favoritesWithAPIInfo:
                Lou = True
            if 'Baton Rouge' in favoritesWithAPIInfo:
                BatonRouge = True
        time.sleep(3)
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


        #   API CLEAN UP / REPORTING
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # # Clean up events and report back on test results
        # delete_place(id1, authToken)
        # delete_place(id2, authToken)
        # delete_place(id3, authToken)
        #
        # # Here we test that the favorite places correctly populated TG-Web
        # assert Elton
        # assert Lou
        # assert BatonRouge
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


if __name__ == '__main__':
    unittest.main()