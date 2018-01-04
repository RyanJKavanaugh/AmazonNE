from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import unittest
import xlrd
import requests
from Variables import WORKBOOKNAMEDATA
from pyvirtualdisplay import Display


class CONSTANTS:
    WORKBOOK = xlrd.open_workbook(WORKBOOKNAMEDATA)
    WORKSHEET = WORKBOOK.sheet_by_index(0)
    URL = WORKSHEET.cell(1, 0).value
    ADJUSTRESOLUTION = WORKSHEET.cell(1, 3).value
    LEGENDDATAWORKSHEET = WORKBOOK.sheet_by_index(2)
    LEGENDDATA = []

    # Create list with relevant Legend data *Check For Each Agency*
    for x in range (1, 9):
        LEGENDDATA.append(LEGENDDATAWORKSHEET.cell(x, 0).value)


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
        "}])); ")
    return driver


class Verify_Legend_Data(unittest.TestCase):


    def test_Legend_Data_Text(self):

        driver = amz_headers_and_return_driver()
        driver.get(CONSTANTS.URL)

        searchButonWait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'mapLegend')))
        mapLegend = driver.find_element_by_id('mapLegend')

        # Assert the legend is hidden initially
        mapLegendDisplay = driver.find_element_by_id('legendContent')
        assert (mapLegendDisplay.get_attribute('style') == 'display: none;')

        # Assert the map legend button is displayed and can be expanded
        assert (mapLegend.is_displayed())
        legendButton = driver.find_element_by_xpath("//*[@title='Toggle Legend']")
        legendButton.click()

        # Verify the correct data is in the map legend
        legendContent = driver.find_element_by_id('legendContent')
        pageData = legendContent.get_attribute("innerHTML")

        # This prints off all the data needed for when switching to a new agency
        # print legendContent.text

        # Run through Legend data list pulled from spreadsheet: *Check For Each Agency*
        for indexNumber in range (0, 8):
            word = CONSTANTS.LEGENDDATA[indexNumber]
            assert word in pageData


if __name__ == '__main__':
    unittest.main()