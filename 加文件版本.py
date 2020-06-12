
#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# %load biotoul_DNA_seq.py
#!/usr/bin/env python

import pandas as pd

familes = [item.split()[0] for item in  pd.read_html('https://www-is.biotoul.fr/Documents/family_characteristics.php')[0][0].to_list() if str(item)!='nan'][1:]


# In[ ]:


familes


# In[ ]:


import requests_html
from selenium import webdriver
from selenium.webdriver.support.select import Select

session = requests_html.HTMLSession()
session.headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "354",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "PHPSESSID=p0865jhgre2du6pd2mcktrks70",
    "DNT": "1",
    "Host": "www-is.biotoul.fr",
    "Origin": "https://www-is.biotoul.fr",
    "Pragma": "no-cache",
    "Referer": "https://www-is.biotoul.fr/search.php",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}

options = webdriver.ChromeOptions()
# options.add_argument(f"--proxy-server={proxy}")
# options.add_argument("headless")
browser = webdriver.Chrome(options=options)


def search(key):
    try:
        browser.get("https://www-is.biotoul.fr/search.php")
        browser.implicitly_wait(30)
        target = Select(browser.find_element_by_xpath('//select[@name="familycond"]'))
        target.select_by_visible_text("equal_to")
        browser.find_element_by_xpath("//input[@name='family']").send_keys(key)
        browser.find_element_by_xpath("//input[@type='submit']").click()
        browser.implicitly_wait(30)
        return pd.read_html(browser.page_source)[0].Name.to_list()
    except Exception as e:
        return []


# In[ ]:


names = {key:search(key) for key in familes}
browser.close()
for k,v in names.items():
    print(k,len(v))


# In[ ]:


import json
js = json.dumps(names)
file = open('test.txt', 'w')
file.write(js)
file.close()


# In[ ]:
import requests_html
import json
file = open('test.txt', 'r') 
js = file.read()
names = json.loads(js)   
print(names) 
file.close()


# In[ ]:
from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd
from progressbar import progressbar
from pathlib import Path
from retry import retry

medias_path = Path('datasets')
medias_path.mkdir(exist_ok=True)

session = requests_html.HTMLSession()
session.headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "354",
    "Content-Type": "application/x-www-form-urlencoded",
    "Cookie": "PHPSESSID=p0865jhgre2du6pd2mcktrks70",
    "DNT": "1",
    "Host": "www-is.biotoul.fr",
    "Origin": "https://www-is.biotoul.fr",
    "Pragma": "no-cache",
    "Referer": "https://www-is.biotoul.fr/search.php",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}


@retry(tries=4)
def save_item(name):
#     name，famliyname，group name，accession number，dna sequence
    filename = medias_path /  f"{name}.csv"
    if filename.exists():
        return
    url = f'https://www-is.biotoul.fr/scripts/ficheIS.php?name={name}'
    resp = session.get(url)
    df = pd.read_html(resp.content)
    pd.DataFrame([{
        'name':name,
        'famliyname':resp.html.pq('#seq_ident > ul > li:nth-child(1)').text().replace('Family','').strip() ,
        'group name': resp.html.pq('#seq_ident > ul > li:nth-child(2)').text().replace('Group','').strip() ,
        'accession number':df[0]['Accession number'][0],
        'dna sequence':resp.html.pq('#page > article > section:nth-child(5) > div:nth-child(1) > div').text().strip(),
        'Origin':df[0]['Origin'][0]
        }]).to_csv(filename)


# In[ ]:


# In[6]:


#save_item('ISAcma3')


# In[ ]:


# In[ ]:


from itertools import chain
[save_item(key) for key in progressbar(list(chain(*names.values())))]

