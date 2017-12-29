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

def post_new_place(placeJson, authToken, headers, accountID):
    apiUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(accountID) + '/customAreas?authTokenId=' + str(authToken)
    newPlacePost = requests.post(apiUrl, json=placeJson, headers=headers)
    data = json.loads(newPlacePost.content)
    id = data.get('id')
    return id


def delete_place(placeID, authToken, headers, accountID):
    deleteUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(accountID) + '/customAreas/' + str(placeID) + '?authTokenId=' + str(authToken)
    deleteItem = requests.delete(deleteUrl, headers = headers)


class Verify_Saved_Places_Via_The_API(unittest.TestCase):

    def test_login(self):

        #   VARIABLES
        userInfo = {"userId":"ryan.kavanaugh@crc-corp.com","password":"test"}
        authTokenURL = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/authTokens'
        headers = {'host': 'hb.511.nebraska.gov'}

        #   JSON FOR CREATING A PLACE
        newPlace = {"accountId":3794,"name":"Broken Bow","normalDuration":None,"polygon":{"type":"Polygon","coordinates":[[[-100.6602479021484,41.20497187153551],[-100.6602479021484,41.60462715035025],[-98.61267099785152,41.60462715035025],[-98.61267099785152,41.20497187153551],[-100.6602479021484,41.20497187153551]]]},"bounds":None,"customAreaShapeSource":"CONFIG_DEFINED","embedded":{},"id":None}
        newPlace2 = {"accountId":3870,"name":"Elmwood, NE, United States","normalDuration":None,"polygon":{"type":"Polygon","coordinates":[[[-97.31812845214847,40.61993337583738],[-97.31812845214847,41.06458509256888],[-95.2705515478516,41.06458509256888],[-95.2705515478516,40.61993337583738],[-97.31812845214847,40.61993337583738]]]},"bounds":None,"customAreaShapeSource":"CONFIG_DEFINED","embedded":{},"id":None}
        newPlace3 = {"accountId":3870,"name":"Callaway","normalDuration":None,"polygon":{"type":"Polygon","coordinates":[[[-101.04807772832027,41.070293961096404],[-101.04807772832027,41.51192081853635],[-98.79450717167964,41.51192081853635],[-98.79450717167964,41.070293961096404],[-101.04807772832027,41.070293961096404]]]},"bounds":None,"customAreaShapeSource":"CONFIG_DEFINED","embedded":{},"id":None}

        myResponse = requests.post(authTokenURL, json=userInfo, headers=headers)
        jData = json.loads(myResponse.content)
        authToken = jData.get('id')
        accountID = jData.get('accountId')

        # print accountID
        # print authToken

        #   GET INITIAL SAVED PLACES VIA API
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        customAreasAPIUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(accountID) + '/customAreas?authTokenId=' + str(authToken)
        customAreaJson = requests.get(customAreasAPIUrl, headers=headers)
        #print customAreaJson.status_code
        data = customAreaJson.json()

        if len(data) > 0:
            # print 'ID 1'
            # print data[0]['id']
            print 'The following places are saved for this user:'
            printCounter = 0
            while printCounter < len(data):
                print printCounter + 1
                print data[printCounter].get('name')
                printCounter+=1
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


        #   CREATE PLACES VIA API
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Calls above function to post new place to the API and ultimately TG Web
        id1 = post_new_place(newPlace, authToken, headers, accountID)
        id2 = post_new_place(newPlace2, authToken, headers, accountID)
        id3 = post_new_place(newPlace3, authToken, headers, accountID)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


        #  VERIFY PLACE IS IN TG WEB
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
        time.sleep(3)
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


        #   API CLEAN UP / REPORTING
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        delete_place(id1, authToken, headers, accountID)
        delete_place(id2, authToken, headers, accountID)
        delete_place(id3, authToken, headers, accountID)
        # Test that the favorite places were present in TG-Web
        assert BrokenBow
        assert Elmwood
        assert Callaway
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


if __name__ == '__main__':
    unittest.main()