# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import unittest
import bs4
import urllib2
from BeautifulSoup import BeautifulSoup
import requests
import xlrd
from Variables import WORKBOOKNAMEDATA
from pyvirtualdisplay import Display
# -*- coding: utf-8 -*-


class CONSTANTS:
    WORKBOOK = xlrd.open_workbook(WORKBOOKNAMEDATA)
    WORKSHEET = WORKBOOK.sheet_by_index(0)
    URL = WORKSHEET.cell(1, 0).value
    ADJUSTRESOLUTION = WORKSHEET.cell(1, 3).value


# Function for Jenkins virtual machine display
def AdjustResolution():
    display = Display(visible=0, size=(800, 800))
    display.start()


if CONSTANTS.ADJUSTRESOLUTION == 1:
    AdjustResolution()


class Verify_Links(unittest.TestCase):


    def test_tg_web_topbar_links(self):

        strList = []
        httpLinkList = []

        # Adding headers to get into the site
        headers = {'host': 'hb.511.nebraska.gov'}

        req = urllib2.Request(CONSTANTS.URL, None, headers)

        html_page = urllib2.urlopen(req)
        soup = BeautifulSoup(html_page)
        allPageLinks = soup.findAll('a', href=True)

        for link in allPageLinks:
            strList.append(str(link['href']))

        for realLink in strList:
            if realLink.startswith('http'):
                httpLinkList.append(realLink)

        counter = 0
        for headerLink in httpLinkList:
            try:
                r = requests.head(headerLink)
                if r.status_code != 200 and r.status_code != 301 and r.status_code != 302:
                    print item
                    counter =+1

            except Exception, e:
                print "failed to connect"
                print headerLink
                print str(e)


        # If there are errors the test will fail here
        if counter > 0:
            assert False


if __name__ == '__main__':
    unittest.main()