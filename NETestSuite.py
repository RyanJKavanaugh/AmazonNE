import unittest
# import HTMLTestRunner
import os
from NEAssertLegend  import Verify_Legend_Data
from NEAssertHeaderLinks import Verify_Links
from NEAssertUserLogin import Verify_Login
from NEAssertCreateAndDeleteViaAPI import Verify_Login_And_Saving_Routes
from NEAssertFDandTextSizes import Verify_Future_Dates_And_Text_Sizes
from NEAssertMapLayers import Verify_Map_Layers
from NEAssertMenuOptions import Verify_Menu_Options
from NEPlacesViaAPI import Verify_Saved_Places_Via_The_API
from NEBothCreateAndDeleteRouteViaAPI import Verify_Login_And_Saving_Routes_Via_API
import xlrd
import sys
from Variables import workbookNameData

workbook = xlrd.open_workbook('DataNE.xlsx')
worksheet = workbook.sheet_by_index(0)
Jenkins = worksheet.cell(1, 4).value

# get the directory path to output report file
dir = os.getcwd()

# get all tests from SearchText and HomePageTest class
#   1
legend = unittest.TestLoader().loadTestsFromTestCase(Verify_Legend_Data)

#   2
header_links = unittest.TestLoader().loadTestsFromTestCase(Verify_Links)

#   3
user_login = unittest.TestLoader().loadTestsFromTestCase(Verify_Login)

#   4
future_dates_and_text_sizes = unittest.TestLoader().loadTestsFromTestCase(Verify_Future_Dates_And_Text_Sizes)

#   5
map_layers = unittest.TestLoader().loadTestsFromTestCase(Verify_Map_Layers)

#   6
create_and_delete_route = unittest.TestLoader().loadTestsFromTestCase(Verify_Login_And_Saving_Routes)

#   7
menu_options = unittest.TestLoader().loadTestsFromTestCase(Verify_Menu_Options)

#   8
saved_place_via_api = unittest.TestLoader().loadTestsFromTestCase(Verify_Saved_Places_Via_The_API)

#   9
create_and_delete_place_via_api = unittest.TestLoader().loadTestsFromTestCase(Verify_Login_And_Saving_Routes_Via_API)

# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([legend, header_links, future_dates_and_text_sizes, map_layers, user_login, create_and_delete_route, menu_options, saved_place_via_api, create_and_delete_place_via_api])

# counter = 0
# numOftimes = 100

if Jenkins == True:
    # run the suite
    # unittest.TextTestRunner(verbosity=2).run(test_suite)
    #unittest.TextTestRunner(verbosity=2).run(test_suite)

    test_runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)
    result = test_runner.run(test_suite)
    sys.exit(not result.wasSuccessful())

else:
    # open the report file
    outfile = open(dir + "\SeleniumPythonTestSummary.html", "w")


    # configure HTMLTestRunner options
    runner = HTMLTestRunner.HTMLTestRunner(stream=outfile,title='Test Report', description='Acceptance Tests')

    # run the suite using HTMLTestRunner
    runner.run(test_suite)