from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

url = "https://leetcode.com/problemset/all/?page="

s = Service('../chromedriver.exe')
driver = webdriver.Chrome(service=s)

def get_a_tags(url):
    driver.get(url)
    time.sleep(7)
    links = driver.find_elements(By.TAG_NAME, "a")
    ans = []
    for link in links:
        try:
            if "/problems/" in link.get_attribute("href"):
                ans.append(link.get_attribute("href"))
        except:
            pass
    ans = list(set(ans))
    return ans

final_ans = []
for i in range (1,56):
    print("Opening page "+str(i))
    final_ans += (get_a_tags(url+str(i)))
    print("Finished scraping page " + str(i) + '\n')
final_ans = list(set(final_ans))

with open('LC_SCRAPE/lc_links.txt', 'a') as f:
    for ans in final_ans:
        f.write(ans+'\n')

print(len(final_ans))

driver.quit()