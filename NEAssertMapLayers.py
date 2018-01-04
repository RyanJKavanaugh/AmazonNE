from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import unittest
import xlrd
from Variables import WORKBOOKNAMEDATA
from pyvirtualdisplay import Display


class CONSTANTS:
    WORKBOOK = xlrd.open_workbook(WORKBOOKNAMEDATA)
    WORKSHEET = WORKBOOK.sheet_by_index(0)
    URL = WORKSHEET.cell(1, 0).value
    ADJUSTRESOLUTION = WORKSHEET.cell(1, 3).value
    VERIFYMAPLAYERSWORKSHEET = WORKBOOK.sheet_by_index(1)

    # Lists for holding Map Layer Data from Spreadsheet
    ITEMTEXT = []
    ITEMLINK = []
    ITEMXPATH = []

    # Loop to gather all relevant agency info into lists for drop down layers
    for x in range (0, 6):
        ITEMTEXT.append(VERIFYMAPLAYERSWORKSHEET.cell(x + 1, 1).value)
        ITEMXPATH.append(VERIFYMAPLAYERSWORKSHEET.cell(x + 1, 2).value)


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


# Function for verifying drop down layers
def Verify_Layer_Drop_Down_Item(driver, xPath, itemText):
    item = driver.find_element_by_xpath(xPath)
    itemHTML = item.get_attribute('innerHTML')
    if (itemText in itemHTML):
        return True
    else:
        return False


class Verify_Map_Layers(unittest.TestCase):


    def test_presence_of_correct_layers(self):
        driver = amz_headers_and_return_driver()

        driver.get(CONSTANTS.URL)

        dropDownMenuWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'layers-menu-dropdown-button')))
        driver.find_element_by_id('layers-menu-dropdown-button').click()

        itemWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layerSelector"]/ul/li[1]/a/span/img[1]')))
        # 1. First Item Verification
        assert Verify_Layer_Drop_Down_Item(driver, CONSTANTS.ITEMXPATH[0], CONSTANTS.ITEMTEXT[0]), (CONSTANTS.ITEMTEXT[0] + " Is Faulty")
        # 2. Second Item Verification
        assert Verify_Layer_Drop_Down_Item(driver, CONSTANTS.ITEMXPATH[1], CONSTANTS.ITEMTEXT[1]), (CONSTANTS.ITEMTEXT[1] + " Is Faulty")
        # 3. Third Item Verification
        assert Verify_Layer_Drop_Down_Item(driver, CONSTANTS.ITEMXPATH[2], CONSTANTS.ITEMTEXT[2]), (CONSTANTS.ITEMTEXT[2] + " Is Faulty")
        # 4. Fourth Item Verification
        assert Verify_Layer_Drop_Down_Item(driver, CONSTANTS.ITEMXPATH[3], CONSTANTS.ITEMTEXT[3]), (CONSTANTS.ITEMTEXT[3] + " Is Faulty")
        # 5. Fifth Item Verification
        assert Verify_Layer_Drop_Down_Item(driver, CONSTANTS.ITEMXPATH[4], CONSTANTS.ITEMTEXT[4]), (CONSTANTS.ITEMTEXT[4] + " Is Faulty")
        # 6. Sixth Item Verification
        assert Verify_Layer_Drop_Down_Item(driver, CONSTANTS.ITEMXPATH[5], CONSTANTS.ITEMTEXT[5]), (CONSTANTS.ITEMTEXT[5] + " Is Faulty")


if __name__ == '__main__':
    unittest.main()