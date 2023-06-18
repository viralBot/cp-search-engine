from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

s = Service('chromedriver.exe')
driver = webdriver.Chrome(service=s)

heading = ".mr-2.text-label-1"
body = ".px-5.pt-4"
index = 1
folder_name = "QDATA"

def get_links():
    links = []
    with open("LC_SCRAPE/lc_problems.txt","r") as f:
        for link in f:
            links.append(link)
    return links

def add_to_file(filename, text):
    file = os.path.join(folder_name, filename)
    if filename == "index.txt":
        with open(file,"a") as f:
            f.write(text+'\n')
    elif filename == "Qindex.txt":
        with open(file,"a",encoding="utf-8",errors="ignore") as f:
            f.write(text)

def add_bodytext_to_file(filename, text):
    folder = os.path.join(folder_name, filename)
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename + ".txt")
    with open(path,"w",encoding="utf-8",errors="ignore") as f:
        f.write(text)

def getData(link, ind):
    try:
        driver.get(link)
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, body)))
        time.sleep(1)
        head = driver.find_element(By.CSS_SELECTOR,heading)
        bod = driver.find_element(By.CSS_SELECTOR,body)
        print(head.text)
        if(head.text):
            add_to_file("index.txt", head.text)
            add_to_file("Qindex.txt", link)
            add_bodytext_to_file(str(ind), bod.text)
        time.sleep(1)
        return True
    except Exception as e:
        print(e)
        return False
    
final_links = get_links()
for link in final_links:
    res = getData(link, index)
    if res:
        index = index + 1

driver.quit()