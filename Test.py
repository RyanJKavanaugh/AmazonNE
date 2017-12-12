from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

url = 'http://crc-prod-ne-tg-elb-1066571327.us-west-2.elb.amazonaws.com/#roadReports?timeFrame=TODAY&layers=allReports%2CroadReports%2CwinterDriving%2CotherStates'

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

driver.get(url)