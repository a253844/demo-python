
import requests
from bs4 import BeautifulSoup
import json
'''
Url_head = 'https://m.momoshop.com.tw/search.momo?searchKeyword='
Url_end = "&couponSeq=&searchType=1&cateLevel=-1&ent=k&_imgSH=fourCardStyle"
USER_AGENT_VALUE = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36'
Query_item = 'Phone+7+Plus+128G'
data = crawler.MOMO_Crawler(Url_head,Url_end,Query_item,USER_AGENT_VALUE)
data.search_momo()
'''

class MOMO_Crawler(object) :
    
    def __init__(self , Url_head , Url_end , Query_item , USER_AGENT_VALUE ):
        self.Url_head = Url_head
        self.Url_end = Url_end
        self.Query_item = Query_item
        self.Query_url = self.Url_head + "%s" + self.Url_end
        self.USER_AGENT_VALUE = USER_AGENT_VALUE
    
    def get_web_content(self) :
        query_url = self.Query_url % self.Query_item  
        headers = {'User-Agent': self.USER_AGENT_VALUE}
        resp = requests.get(query_url, headers=headers)
        if not resp:
            return []
        resp.encoding = 'UTF-8'
        resp = BeautifulSoup(resp.text, 'html.parser')
        return resp
    
    def search_momo(self):
        items = []
        dom = self.get_web_content()
        product = dom.find_all('li',class_='goodsItemLi')
        print(product)
        for i in range(len(product)): 
            items.append(product[i].find('p',class_='prdName').text)
            items.append(product[i].find('b',class_='price').text)
        #print(product[0].find('p',class_='prdName').text)
        #print(product[0].find('b',class_='price').text)
        print(items)

"""
url = "https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=ASUS%20ZenFone%20Max%20Pro%20M2&page=1&sort=prc/dc"
get_project = crawler.PChome_Crawler(url)
print(get_project.search_pchome())
"""
class PChome_Crawler(object) :  
    
    def __init__(self, url):
        self.url = url
        
    def search_pchome(self):
        res = requests.get(self.url)
        data = json.loads(res.text)
        webdata = data["prods"]
        product = []
        for i in  webdata :
            if int(i["price"]) <5000 :
                break
            product.append(i["name"])
            product.append(i["price"])
        return product
