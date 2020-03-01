
import requests
from bs4 import BeautifulSoup
import json
import time , datetime

class google_Crawler(object) :
    
    def __init__(self , Url_head , Url_end , URL_date , Query_item , USER_AGENT_VALUE , URL_pgae ):
        self.Url_head = Url_head
        self.Url_end = Url_end
        self.Query_item = Query_item
        self.URL_date = URL_date
        self.URL_pgae = URL_pgae
        self.Query_url = self.Url_head + self.Query_item + self.Url_end + self.URL_date + self.URL_pgae
        self.USER_AGENT_VALUE = USER_AGENT_VALUE
    
    def get_web_content(self) :
        query_url = self.Query_url   
        headers = {'User-Agent': self.USER_AGENT_VALUE}
        resp = requests.get(query_url, headers=headers )
        if not resp:
            return []
        resp.encoding = 'UTF-8'
        resp = BeautifulSoup(resp.text, 'html.parser')
        print(query_url)
        return resp
    
    def search_google(self):
        items = []
        dom = self.get_web_content()
        product = dom.find_all('g-card',class_='CFbRHb')
        
        for i in range(len(product)): 
            data = []
            if product[i].find('div',class_='VHVT3c').find('img')['alt'] != '' :
                data.append(product[i].find('div',class_='VHVT3c').find('img')['alt'])
            else:
                data.append(product[i].find('div' , class_="VHVT3c").text)
            data.append(product[i].find('div',class_='ZUdMOb').text)
            data.append(product[i].find('a')['href'])
            data.append(product[i].find('span',class_='pBrkfd').text)
            items.append(data)
        #print(product[i].find('div',class_='VHVT3c').find('img')['alt'])
        #print(product[0].find('b',class_='price').text)
        
        return items
    

Url_head = 'https://www.google.com'
Query_item = '/search?q=武漢肺炎'
Url_end = "&safe=strict&tbas=0&tbs=qdr:d"
URL_date = "cd_min:{date},cd_max:{date}" #m/d/y e.g2/20/2020
URL_pgae = '&tbm=nws&sxsrf=ALeKk01lbnPspzl32seybDsR42NiLqXpXg:1582615459681&ei=o8tUXrqWKZmB-QbJqp3IAQ&start=' # 0 10 20
USER_AGENT_VALUE = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36'

#date = '1/13/2020'
#URL_date = URL_date.format(date=date)
#page = str(0)
#data = google_Crawler(Url_head,Url_end,URL_date,Query_item,USER_AGENT_VALUE , URL_pgae )
#d_list = data.search_google()

#page = '1'

#-----------------------------------------------------------
import pymysql

insert_data = "insert into news (Company,Topic,url,date) value"
#date =''
newsday=time.strftime("%Y/%m/%d", time.localtime())
#URL_dates = URL_date.format(date=date)
URL_dates =''
now = datetime.datetime.now().strftime('%H')

while True : 
    db = pymysql.connect(host="",
                 user="root", 
                 passwd="", 
                 db="dbtest")
    cursor = db.cursor()
    for i in range(50):
        URL_pgaes = URL_pgae + str(i) + '0'
    
        data = google_Crawler(Url_head,Url_end,URL_dates,Query_item,USER_AGENT_VALUE , URL_pgaes )
        d_list = data.search_google()
        
        for i in range(len(d_list)):
            try:
                if d_list[i][3].find('分鐘') >0 :
                    insert = "('"+d_list[i][0]+"','"+d_list[i][1]+"','"+d_list[i][2]+"','"+newsday+"');"
                    data = insert_data+insert
                    cursor.execute(data)
                    db.commit()
                elif d_list[i][3].find('小時') >0 and int(d_list[i][3][0:d_list[i][3].find('小時')])<int(now):
                    insert = "('"+d_list[i][0]+"','"+d_list[i][1]+"','"+d_list[i][2]+"','"+newsday+"');"
                    data = insert_data+insert
                    cursor.execute(data)
                    db.commit()
            except:
                continue
        if d_list == [] :
            break
            
    cursor.close()
    db.close()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    time.sleep(600)
       




    
