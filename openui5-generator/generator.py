import os
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys

dirname = os.path.dirname(os.path.realpath(__file__))

img_dir = '_img_test/'
page_dir = '_xml_test/'
openui5_dir = '/Users/florian/projects/openui5/openui5/src/sap.m/test/basicTemplate/webapp/view/'

url = 'http://localhost:8080/test-resources/basicTemplate/webapp/index.html'

num_elements = 8
start= 0
end = 20

wait_for_element = '__button0'

def generate_page():
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



def save_page(path):
    with open(path, 'w') as f:
        for item in page:
            f.write("%s\n" % item)

i = start
while i < end:
    print(str(i))
    page = generate_page()

    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    driver.set_window_size(600, 600)
    driver.get(url)
    timeout = 5
    save_page(openui5_dir+'App.view.xml')

    try:
        element_present = EC.presence_of_element_located((By.ID, wait_for_element))
        WebDriverWait(driver, timeout).until(element_present)

        filename = str(i).zfill(4)
        img_path = os.path.join(dirname, img_dir+filename+'.png')
        driver.save_screenshot(img_path)

        page_path = os.path.join(dirname, page_dir+filename+'.xml')
        save_page(page_path)
        
        i += 1
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        driver.quit()

    
    




    

