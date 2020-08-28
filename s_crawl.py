from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import numpy as np

url = 'https://www.mylittletiger.co.kr/good/category/IA0000'

driver = webdriver.Chrome()
driver.get(url)
time.sleep(3)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

li_tag = soup.select('.listWrap li')

product_list = []

# print(len(ul))
# print(ul)
for li in li_tag:
    product = []
    try:
        product.append(li.select_one('.h1').text)
        product.append(li.select_one('.h2').text)
        product.append(li.select_one('.list_sale').text)
    except:
        pass

    if product == []:
        pass
    else: 
        product_list.append(product)

import pandas as pd 
df = pd.DataFrame(product_list)
print(df)