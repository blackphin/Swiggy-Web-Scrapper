# Imports
from time import sleep
import pickle, json, pyautogui

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


# WebDriver Initialization
options = Options()
options.add_argument("start-maximized")
# options.add_argument(
#     {"user-data-dir": r"C:\Users\shiva\AppData\Local\Google\Chrome\User Data\Default"}
# )
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)
pyautogui.hotkey("win", "d")
pyautogui.hotkey("alt", "tab")
pyautogui.hotkey("alt", "tab")


# Login Sequence
# driver.get("https://www.swiggy.com")
# driver.find_element(by=By.LINK_TEXT, value="Login").click()
# driver.find_element(by=By.NAME, value="mobile").send_keys("9318335215")
# driver.find_element(by=By.NAME, value="mobile").send_keys(Keys.ENTER)
# sleep(20)
# driver.find_element(by=By.CLASS_NAME, value="_24Etq").click()


# Location Sequence
driver.get("https://swiggy.com")
driver.find_element(by=By.NAME, value="location").send_keys(
    "Dwarka Sector 11, Dwarka, Delhi, India"
)
sleep(2)
driver.find_element(by=By.CLASS_NAME, value="_2W-T9").click()
sleep(2)


# Scroll to the Bottom
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script(
        "window.scrollTo({top: document.body.scrollHeight-7000,left: 0,behavior: 'smooth'});"
    )

    # Wait to load page
    sleep(scroll_pause_time)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


# Create Restraunt's Links List
no_of_restraunts = driver.find_element(by=By.CLASS_NAME, value="BZR3j").text[0:-12]
restraunt_elements_list = driver.find_elements(by=By.CSS_SELECTOR, value=".undefined a")
restraunt_links_list = []
for restraunt_element in restraunt_elements_list:
    if (
        restraunt_element.get_attribute("href") != "https://www.swiggy.com/search"
        and restraunt_element.get_attribute("href") != None
    ):
        restraunt_links_list.append(restraunt_element.get_attribute("href"))

print(f"Restraunts Found: {len(restraunt_links_list)}/{no_of_restraunts}")

with open("restraunt_links_list.log", "wb") as file1:
    pickle.dump(restraunt_links_list, file1)


# Verify Restraunt's Links List
with open("restraunt_links_list.log", "rb") as file1:
    restraunt_links_list = pickle.load(file1)
print(f"Links Saved: {len(restraunt_links_list)}")
# print(restraunt_links_list)


# Collect Data
data = []
for restraunt_number in range(0, 10):
    restraunt_data = {}

    driver.get(restraunt_links_list[restraunt_number])

    restraunt_data["restraunt_name"] = driver.find_element(
        by=By.CLASS_NAME, value="_3aqeL"
    ).text
    restraunt_data["restraunt_category"] = (
        driver.find_element(by=By.CLASS_NAME, value="JMACF").text
    ).split(", ")
    restraunt_data["restraunt_address"] = driver.find_element(
        by=By.CLASS_NAME, value="_2Y6HW"
    ).text

    info_list = driver.find_elements(by=By.CSS_SELECTOR, value="._2fC4N div div span")

    restraunt_data["rating"] = info_list[0].text
    restraunt_data["delivery time"] = info_list[3].text[:-5]
    restraunt_data["average_cost"] = info_list[4].text[2:]

    """
    Collect Data (2)
    """

    restraunt_data["menu"] = []
    category_class_list = driver.find_elements(
        by=By.CSS_SELECTOR, value="._1J_la ._2dS-v"
    )
    category_id_list = []
    for category_class in category_class_list:
        category_id_list.append(category_class.get_attribute("id"))
    for category_id in category_id_list:
        category_data = {}
        category_data["category_name"] = driver.find_element(
            by=By.CSS_SELECTOR, value=f"._1J_la #{category_id} .M_o7R"
        ).text
        category_data["sub_categories"] = []
        sub_category_class_list = driver.find_elements(
            by=By.CSS_SELECTOR, value=f"._1J_la #{category_id} ._1Jgt5"
        )
        sub_category_id_list = []
        for sub_category_class in sub_category_class_list:
            sub_category_id_list.append(sub_category_class.get_attribute("id"))
        for sub_category_id in sub_category_id_list:
            sub_category_data = {}
            sub_category_data["sub_category_name"] = driver.find_element(
                by=By.CSS_SELECTOR,
                value=f"._1J_la #{category_id} #{sub_category_id} ._2WzQq",
            ).text
            sub_category_data["items"] = []
            item_name_list = driver.find_elements(
                by=By.CSS_SELECTOR,
                value=f"._1J_la #{category_id} #{sub_category_id} .styles_itemNameText__3ZmZZ",
            )
            item_price_list = driver.find_elements(
                by=By.CSS_SELECTOR,
                value=f"._1J_la #{category_id} #{sub_category_id} .rupee",
            )
            item_desc_list = driver.find_elements(
                by=By.CSS_SELECTOR,
                value=f"._1J_la #{category_id} #{sub_category_id} .styles_itemDesc__3vhM0",
            )
            for item_no in range(0, len(item_name_list)):
                item_data = {}
                item_data["item_name"] = item_name_list[item_no].text
                item_data["item_price"] = item_price_list[item_no].text
                # item_data["item_desc"]=item_desc_list[item_no]
                sub_category_data["items"].append(item_data)
            category_data["sub_categories"].append(sub_category_data)
        restraunt_data["menu"].append(category_data)
    data.append(restraunt_data)

json_data = json.dumps(data, indent=4)
# print(json_data)


# Store Data to JSON File
with open("data.json", "w") as file2:
    json.dump(data, file2)


# Quit WebDriver
driver.quit()
