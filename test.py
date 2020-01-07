from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("http://www.baidu.com")
driver.maximize_window()
try:
#为了更好的对比效果，首先我们设置了一个存在的元素，然后在去找一个不存在的元素，同样设置了10s的等待时间
#kw元素存在时
    print(datetime.now())  #
    element = WebDriverWait(driver,10).until(   #until 也属于WebDriverWait,代表一直等待,直到某元素可见，until_not与其相反，判断某个元素直到不存在
    EC.presence_of_element_located((By.ID, "kw"))  #presence_of_element_located主要判断页面元素kw在页面中存在。
)
#kw111元素不存在时
    print(datetime.now())
    element = WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.ID, "kw111"))
)


finally:
    print(datetime.now())
    driver.quit()