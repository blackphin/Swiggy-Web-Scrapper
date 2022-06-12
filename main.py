from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

webdriver_timeout = 10  # seconds

options = Options()
options.add_argument("start-maximized")
# options.add_argument(
#     {"user-data-dir": r"C:\Users\shiva\AppData\Local\Google\Chrome\User Data\Default"}
# )

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
driver.get("https://www.swiggy.com")
driver.maximize_window()
driver.find_element(by=By.LINK_TEXT, value="Login").click()
driver.find_element(by=By.NAME, value="mobile").send_keys("9318335215")
driver.find_element(by=By.NAME, value="mobile").send_keys(Keys.ENTER)
sleep(15)


no_of_restraunts = driver.find_element(by=By.CLASS_NAME, value="BZR3j").text[0:-12]
restraunt_list = driver.find_elements(by=By.CSS_SELECTOR, value=".undefined a")
restraunt_links = []
for restraunt in restraunt_list:
    restraunt_links.append(restraunt.get_attribute("href"))

driver.get(restraunt_links[1])

data = []

for restraunt in range(1, len(restraunt_links)):
    restraunt_1 = {}

    restraunt_1["name"] = driver.find_element(by=By.CLASS_NAME, value="_3aqeL").text
    restraunt_1["category"] = (
        driver.find_element(by=By.CLASS_NAME, value="JMACF").text
    ).split(",")
    restraunt_1["address"] = driver.find_element(by=By.CLASS_NAME, value="_2Y6HW").text

    info_list = driver.find_elements(by=By.CSS_SELECTOR, value="._2fC4N div div span")

    restraunt_1["rating"] = info_list[0].text
    restraunt_1["delivery time"] = info_list[3].text
    restraunt_1["average_cost"] = info_list[4].text

    data.append(restraunt_1)
# driver.close()
driver.quit()
print(data)
