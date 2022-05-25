import time
import byPassCaptcha as bypass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager

import json

# Define main parameters
path        = 'D:/NFT/Dinos/'
path_images = path + 'images/'
path_meta   = path + 'metadata/'
image_extension = '.png'
json_extension  = '.json'

collection = 'dinos-with-boots'

total_number = 10000 #The total amount of NFTs in your collection

TIMEOUT = 30
PING    = 1

# Programmatically launch a Chrome browser and navigate to OpenSea:
opensea = 'https://opensea.io'

options = webdriver.ChromeOptions()
options.add_argument("--disable-infobars")
options.add_argument('--disable-notifications')
options.add_argument("--mute-audio")
options.add_argument("--enable-file-cookies")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_extension('C:\\Users\\serha\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\nkbihfbeogaeaoehlefnkodbefgpgknn\\10.11.1_0.crx') #the version may vary

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
browser.maximize_window()
browser.switch_to.window(browser.window_handles[0])


def wait_any_element_to_have_text(xpath, text, wait_time=TIMEOUT):
    """
    Wait until text is present in element:
    Most web apps are using AJAX techniques, so when a page is loaded by the browser,
    the elements within that page may load at different time intervals, which makes locating elements tricky:
    if an element is not yet present in the DOM,
    the find_elements function will raise an exception. As such we wait until the pre-defined timeout, before we break.
    :param xpath:
    :param text:
    :param wait_time:
    :return:
    """
    secs_passed = 0
    while secs_passed < wait_time:
        elements = browser.find_elements(By.XPATH, xpath)
        for element in elements:
            if element.text == text:
                return element

        time.sleep(PING)
        secs_passed += PING


def center_and_click(element):
    """
    Locate an element and click on it:
    Again, sometimes the element we want to click may not be visible,
    so after locating it, we centre the surrounding screen, and then click it:
    :param element:
    :return:
    """
    script = """
        var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
        var elementTop = arguments[0].getBoundingClientRect().top;
        window.scrollBy(0, elementTop-(viewPortHeight / 2));
        """

    browser.execute_script(script, element)
    element.click()
    return element


def write_text(element, text):
    """
    Write text on input field:
    The code below also handles unicode characters, like emoji 🦸‍♀️:
    :param element:
    :param text:
    :return:
    """
    script = """
        var element = arguments[0], txt = arguments[1];
        element.value = txt;
        element.innerHTML = txt;
        element.dispatchEvent(new Event('change'));
        """

    text = text.replace("\\n", "\n")
    browser.execute_script(script, element, text)
    element.send_keys(" " + Keys.BACKSPACE)


def read_token_info(token):
    """
    Lazy Minting
    Read token’s metadata:
    1. Reads the json file for a given token id, and
    2. accesses the relevant json elements and returns them in a tuple.
    :param token:
    :return:
    """
    data = []
    with open(path_meta + str(token) + json_extension, "r") as jsonfile:
        try:
            data = json.load(jsonfile)
        except:
            data = []

    token_name = data['name']
    token_description = data['description']
    token_properties = data['attributes']

    return (token_name, token_description, token_properties)


def mint_token(token):
    """
    Mint one: This method:
    1. first navigates to the collection’s create endpoint,
    2. uploads the NFT picture,
    3. calls the read_token_info function to get the token’s metadata, and sets the name,
        description and all the properties [n.b.: The first property is always set,
        so it presses the Add more button for properties_number - 1 times],
    4. creates the NFT, and
    5. awaits for confirmation.
    :param token:
    :return:
    """
    time.sleep(PING)
    browser.switch_to.window(browser.window_handles[0])
    time.sleep(PING)
    browser.get(opensea + '/collection/' + collection + '/assets/create')

    time.sleep(2)
    # Add media
    media = browser.find_element(By.ID, "media")
    browser.execute_script("arguments[0].style.display = 'block';", media)
    media.send_keys(path_images + str(token) + image_extension)

    # Read token's metadata
    token_info = read_token_info(token)
    token_name = token_info[0]
    token_description = token_info[1]
    token_properties = token_info[2]
    properties_number = len(token_properties)

    # Add name
    name = browser.find_element(By.ID, "name")
    write_text(name, token_name)

    # Add description
    description = browser.find_element(By.ID, "description")
    write_text(description, token_description)

    # Add properties
    properties = browser.find_element(By.XPATH, "//div[@class='AssetFormTraitSection--item']//i[@value='add']")
    properties.click()

    addmore = browser.find_element(By.XPATH, "//button[text()='Add more']")
    for i in range(properties_number - 1):
        addmore.click()
        time.sleep(PING)

    type_inputs = browser.find_elements(By.XPATH, "//input[@placeholder='Character']")
    name_inputs = browser.find_elements(By.XPATH, "//input[@placeholder='Male']")

    for i, prop in enumerate(token_properties):
        type_inputs[i].send_keys(prop["trait_type"])
        name_inputs[i].send_keys(prop["value"])

    save = browser.find_element(By.XPATH, "//button[text()='Save']")
    center_and_click(save)
    time.sleep(PING)

    # Finally Create
    create = browser.find_element(By.XPATH, "//button[text()='Create']")
    center_and_click(create)
    time.sleep(PING)

    # call byPassCaptcha.py to bypass captcha
    bypass.start_bypassing(browser, opensea + '/collection/' + collection + '/assets/create')
    # browser.switch_to.window(browser.window_handles[0])

    # And wait for confirmation
    # minted = wait_any_element_to_have_text("//h4", 'You created ' + token_name + '!')
    return True
    # return (minted is not None)


def connect_metamask_to_opensea(browser):
    browser.find_element(By.XPATH, '//span[text()="MetaMask"]').click()
    # For now you have to click to select the wallets, it's seems it's not working now.
    time.sleep(2)
    browser.switch_to.window(browser.window_handles[2])
    browser.find_element(By.XPATH, '//button[text()="Next"]').click()
    time.sleep(1)
    browser.find_element(By.XPATH, '//button[text()="Connect"]').click()


def sign_metamask_to_opensea(browser):
    browser.find_element(By.XPATH, '//span[text()="MetaMask"]').click()
    # For now you have to click to select the wallets, it's seems it's not working now.
    time.sleep(2)
    browser.switch_to.window(browser.window_handles[2])
    browser.find_element(By.XPATH, '//button[text()="Sign"]').click()


time.sleep(1)
browser.find_element(By.XPATH, '//button[text()="Get Started"]').click()
time.sleep(1)
browser.find_element(By.XPATH, '//button[text()="Import wallet"]').click()
time.sleep(1)
browser.find_element(By.XPATH, '//button[text()="No Thanks"]').click()
time.sleep(1)

# After this you will need to enter you wallet details

inputs = browser.find_elements(By.XPATH, '//input')
inputs[0].send_keys(PRIVATE_KEY)
inputs[2].send_keys(PASSWORD)
inputs[3].send_keys(PASSWORD)
# check a checkbox
inputs[4].click()
time.sleep(1)
browser.find_element(By.XPATH, '//button[text()="Import"]').click()
time.sleep(2)
browser.find_element(By.XPATH, '//button[text()="All Done"]').click()
time.sleep(1)

browser.get(opensea + '/login')

connect_metamask_to_opensea(browser)
time.sleep(1)

browser.switch_to.window(browser.window_handles[0])
browser.get(opensea + '/collection/' + collection + '/assets/create')
time.sleep(2)
sign_metamask_to_opensea(browser)


if __name__ == '__main__':
    # Mint them all:
    # Now loop through all your NFTs and mint them by calling the mint_token function:

    token_start = 6
    token_end = total_number

    # current_page = browser.current_window_handle

    for i in range(token_start, token_end + 1):
        try:
            is_minted = mint_token(i)
            if not is_minted:
                raise Exception('Token ' + str(i) + ' not minted!')
            time.sleep(PING)

        except Exception as e:
            raise

    browser.switch_to.window(current_page)
