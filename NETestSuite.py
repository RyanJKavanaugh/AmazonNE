import unittest
import os
from NEAssertLegend  import Verify_Legend_Data
from NEAssertHeaderLinks import Verify_Links
from NEAssertUserLogin import Verify_Login
from NEAssertCreateViaAppAndDeleteViaAPI import Verify_Login_And_Saving_Routes
from NEAssertFutureDatesandTextSizes import Verify_Future_Dates_And_Text_Sizes
from NEAssertMapLayers import Verify_Map_Layers
from NEAssertMenuOptions import Verify_Menu_Options
from NEAssertPlacesViaAPI import Verify_Saved_Places_Via_The_API
from NEAssertBothCreateAndDeleteRouteViaAPI import Verify_Login_And_Saving_Routes_Via_API
import xlrd
import sys
from Variables import WORKBOOKNAMEDATA

WORKBOOK = xlrd.open_workbook(WORKBOOKNAMEDATA)
WORKSHEET = WORKBOOK.sheet_by_index(0)


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


# Complete test suite
test_suite = unittest.TestSuite([legend, header_links, user_login, future_dates_and_text_sizes, map_layers, create_and_delete_route, menu_options, saved_place_via_api, create_and_delete_place_via_api])


# Run the test suite so that it reports fails at the very end
test_runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)
result = test_runner.run(test_suite)
sys.exit(not result.wasSuccessful())
