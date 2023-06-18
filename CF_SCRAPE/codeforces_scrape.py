from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import chardet

def find_encoding(file):
    r_file = open(file, 'rb').read()
    res = chardet.detect(r_file)
    charenc = res['encoding']
    return charenc

url = "https://codeforces.com/problemset/page/"

s = Service('chromedriver.exe')
driver = webdriver.Chrome(service=s)

def get_a_tags(url):
    driver.get(url)
    time.sleep(5)
    links = driver.find_elements(By.TAG_NAME, "a")
    ans = []
    for link in links:
        try:
            if ("/problem/" in link.get_attribute("href")) and ("/status/" not in link.get_attribute("href")):
                ans.append(link.get_attribute("href"))
        except:
            pass
    ans = list(set(ans))
    return ans

final_ans = []
for i in range (1,89):
    print("Opening page "+str(i))
    final_ans += (get_a_tags(url+str(i)))
    print("Finished scraping page " + str(i) + '\n')
final_ans = list(set(final_ans))

with open('CF_SCRAPE/cf_links.txt', 'w',encoding = find_encoding('CF_SCRAPE/cf_links.txt'), errors="ignore") as f:
    for ans in final_ans:
        f.write("%s\n" % ans)

print(len(final_ans))

driver.quit()