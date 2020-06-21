import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#caps = DesiredCapabilities.CHROME
#caps['loggingPrefs'] = {'performance': 'ALL'}
# 78版本的chrome需要加这个，https://stackoverflow.com/questions/56812190/protractor-log-type-performance-not-found-error
caps = {
    'browserName': 'chrome',
    'loggingPrefs': {
        'browser': 'ALL',
        'driver': 'ALL',
        'performance': 'ALL',
    },
    'goog:chromeOptions': {
        'perfLoggingPrefs': {
            'enableNetwork': True,
        },
        'w3c': False,
    },
}
driver = webdriver.Chrome(desired_capabilities=caps)

url = 'https://search.earthdata.nasa.gov/search/granules?p=C1214471521-ASF!C1327985660-ASF&pg[1][v]=t&q=GRD&sb=-180%2C62.88638545512935%2C178.875%2C90&m=-104.90889844363065!-88.3125!0!1!0!0%2C2&qt=2016-01-01T00%3A00%3A00.000Z%2C2016-01-10T23%3A59%3A59.999Z&tl=1559463941!4!!'

driver.get(url)

# logs = [json.loads(log['message'])['message'] for log in driver.get_log('performance')]

for log in driver.get_log('performance'):
    print(json.loads(log['message'])['message'])

# with open('devtools.json', 'wb') as f:
#     json.dump(logs, f)

driver.close()