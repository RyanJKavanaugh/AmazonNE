from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.by import By
import xlrd
import time
import unittest
import os
from Variables import WORKBOOKNAMEDATA
from pyvirtualdisplay import Display

# Test verifies the Future Info Toolbar buttons are fully functional
# Required Function For Working With Jenkins Virtual Machine


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


def amz_headers_and_return_driver():
    options = webdriver.ChromeOptions()
    options.add_extension('ModHeader_v2.1.2.crx')
    driver = webdriver.Chrome(chrome_options=options)
    driver.maximize_window()

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


class Verify_Future_Dates_And_Text_Sizes(unittest.TestCase):


    def test_Future_Info_Toolbar_Is_Active(self):
        driver = amz_headers_and_return_driver()

        driver.get(CONSTANTS.URL)

        loginElement = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'timeFrameSelectorDiv')))

        driver.find_element_by_id('timeFrameSelectorDiv').click()

        time.sleep(6)

        assert driver.find_element_by_id('timeFrameSelectorDiv').is_enabled()

        assert driver.find_element_by_id('smallTextLnk').is_enabled()

        assert driver.find_element_by_id('normalTextLnk').is_enabled()

        assert driver.find_element_by_id('largeTextLnk').is_enabled()

        assert driver.find_element_by_id('textOnlySiteLinkSpan').is_enabled()


if __name__ == '__main__':
    unittest.main()

