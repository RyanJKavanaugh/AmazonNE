# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common import action_chains, keys
import time
import unittest
import xlrd
from pyvirtualdisplay import Display
from Variables import WORKBOOKNAMEDATA
# -*- coding: utf-8 -*-


# Function for Jenkins virtual machine display
def AdjustResolution():
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


class Verify_Menu_Options(unittest.TestCase):

    def setUp(self):
        # Includes options for the ModHeader chrome extension
        options = webdriver.ChromeOptions()
        options.add_extension('ModHeader_v2.1.2.crx')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.maximize_window()


    def test_Menu_Options(self):

        driver = self.driver
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
        driver.get(CONSTANTS.URL)

        # Login To The System
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'sign-in-link')))
        driver.find_element_by_id('sign-in-link').click()
        driver.find_element_by_id('userAccountEmail').send_keys(CONSTANTS.USERNAME)
        driver.find_element_by_id('userAccountPassword').send_keys(CONSTANTS.PASSWORD)
        driver.find_element_by_id('userAccountPassword').submit()

        # Check that all menu items are present
        left_Panel_Wait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@title="Ryan’s Favorites"]')))
        # 1
        assert (driver.find_element_by_xpath('//*[@title="Ryan’s Favorites"]').is_enabled()) == True, "Favorites Is Faulty"
        # 2
        assert driver.find_element_by_xpath("//*[contains(text(), 'All Reports')]").is_enabled(), "All Reports Is Faulty"
        # 3
        assert driver.find_element_by_xpath('//*[@title="See maps and lists of cameras and view camera images"]').is_enabled(), "Cameras Is Faulty"
        # 4
        assert driver.find_element_by_xpath('//*[@title="See up-to-date traffic conditions"]').is_enabled(), "Traffic Speeds Is Faulty"
        # 5
        assert driver.find_element_by_xpath('//*[@title="See maps and lists of weather stations and review weather data"]').is_enabled(), "Weather Stations Is Faulty"


    def tearDown(self):
         self.driver.quit()


if __name__ == '__main__':
    unittest.main()
