import re

links = []
with open("lc_links.txt","r") as f:
    for link in f:
        links.append(link[:len(link)-1])

def remove_links_with_pattern(arr, pattern):
    res = []
    for element in arr:
        if pattern not in element:
            res.append(element)
        else:
            print("Removed: " + element)
    return res

links = remove_links_with_pattern(links,"/solution")
links = list(set(links))
print(len(links))

with open('lc_problems.txt', 'a') as f:
    for link in links:
        f.write(link+'\n')