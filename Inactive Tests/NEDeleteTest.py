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

def delete_place(placeID, authToken):
    headers = {'host': 'hb.511.nebraska.gov'}
    deleteUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/3763/trips/' + str(placeID) + '?authTokenId=' + str(authToken)
    deleteItem = requests.delete(deleteUrl, headers=headers)
    print deleteItem.status_code


class Verify_Saved_Places_Via_The_API(unittest.TestCase):


    def test_login(self):
        #   VARIABLES
        userInfo = {"userId":"ryan.kavanaugh@crc-corp.com","password":"test"}
        authTokenURL = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/authTokens'
        headers = {'host': 'hb.511.nebraska.gov'}

        myResponse = requests.post(authTokenURL, json=userInfo, headers=headers)
        jData = json.loads(myResponse.content)
        authToken = jData.get('id')
        accountID = jData.get('accountId')
        #   GET INITIAL SAVED PLACES VIA API (do I really need this ??? )
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # 777 Gets the user's current saved places and prints them out:
        customAreasAPIUrl = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/tgpublicaccounts/api/accounts/' + str(accountID) + '/trips?authTokenId=' + str(authToken)
        customAreaJson = requests.get(customAreasAPIUrl, headers=headers)
        data = customAreaJson.json()
        indexNumber = 0
        if len(data) > 0:
            for x in data:
                routeID = data[indexNumber].get('id')
                delete_place(routeID, authToken)
                indexNumber += 1


if __name__ == '__main__':
    unittest.main()