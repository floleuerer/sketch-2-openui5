import os
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys

dirname = os.path.dirname(__file__)

num_elements = 8 
start= 0
samples = 5000

def generate_file():
    tok_start = "<!--START-->\n<mvc:View displayBlock=\"true\" xmlns=\"sap.m\" xmlns:mvc=\"sap.ui.core.mvc\">\n<VBox class=\"sapUiSmallMargin\">"
    tok_end = "</VBox>\n</mvc:View>\n<!--END-->"

    tokens = []
    tokens.append("<RadioButton groupName=\"GroupA\" text=\"Option 1\" selected=\"true\" />")
    tokens.append("<RadioButton groupName=\"GroupA\" text=\"Option 2\" />")
    tokens.append("<Switch state=\"true\" />")
    tokens.append("<Input width=\"250px\" class=\"sapUiSmallMarginBottom\" />")
    tokens.append("<CheckBox text=\"Option a\" selected=\"true\" />")
    tokens.append("<CheckBox text=\"Option b\" />")
    tokens.append("<Button text=\"Default\" />")
    tokens.append("<Button text=\"Accept\" type=\"Accept\" />")
    tokens.append("<Slider value=\"40\" width=\"15em\" class=\"sapUiSmallMarginBottom\" />")

    page = []

    page.append(tok_start)

    for i in range(num_elements):
        rnd = random.randrange(len(tokens))
        page.append(tokens[rnd])

    page.append(tok_end)
    
    return page

def get_screenshot(filename):
    options = Options()
    options.add_argument( "--headless" )
    driver = webdriver.Firefox( firefox_options=options )
    driver.set_window_size(600, 600)
    driver.get('http://localhost:8080/test-resources/basicTemplate/webapp/index.html')
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.ID, '__button0'))
        WebDriverWait(driver, timeout).until(element_present)
        filename = os.path.join(dirname, filename)
        driver.save_screenshot(filename)
    except TimeoutException:
        print("Timed out waiting for page to load")
    driver.quit()


def save_page(filename):
    filename = os.path.join(dirname, filename)
    with open(filename, 'w') as f:
        for item in page:
            f.write("%s\n" % item)


for i in range(start,samples):
    print(str(i))
    page = generate_file()

    save_page('App.view.xml')
    save_page('_xml/'+str(i)+'.xml')
    get_screenshot('_img/'+str(i)+'.png')



    






