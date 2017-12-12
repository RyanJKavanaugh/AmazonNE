# coding=utf-8
from selenium import webdriver
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
from Variables import workbookNameData
from pyvirtualdisplay import Display
# -*- coding: utf-8 -*-


def AdjustResolution():
    display = Display(visible=0, size=(800, 800))
    display.start()


workbook = xlrd.open_workbook(workbookNameData)
worksheet = workbook.sheet_by_index(0)
url = worksheet.cell(1, 0).value
adjustResolution = worksheet.cell(1, 3).value


if adjustResolution == 1:
    AdjustResolution()


class Verify_Links(unittest.TestCase):


    def test_tg_web_topbar_links(self):
        strList = []
        httpLinkList = []

        # Adding headers to get into the site
        headers = {'host': 'hb.511.nebraska.gov'}
        req = urllib2.Request(url, None, headers)

        html_page = urllib2.urlopen(req)
        soup = BeautifulSoup(html_page)
        allPageLinks = soup.findAll('a', href=True)

        for link in allPageLinks:
            strList.append(str(link['href']))

        for realLink in strList:
            if realLink.startswith('http'):
                httpLinkList.append(realLink)

        counter = 0
        for item in httpLinkList:
            # print item
            try:
                r = requests.head(item)
                if r.status_code != 200 and r.status_code != 301 and r.status_code != 302:
                    print item
                    counter =+1


            except Exception, e:
                print "failed to connect"
                print item
                print str(e)


        if counter > 0:
            assert False


if __name__ == '__main__':
    unittest.main()