import requests
from bs4 import BeautifulSoup
import json
import csv , time , copy

start = time.time()

USER_AGENT_VALUE = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36'
query_url = 'https://www.sogi.com.tw'
page_url = '/brands'

def Get_brands_url (USER_AGENT_VALUE , query_url , page_url):
    headers = {'User-Agent': USER_AGENT_VALUE }
    resp = requests.get(query_url + page_url, headers=headers)
    if not resp:
        print("None")

    resp.encoding = 'UTF-8'
    resp = BeautifulSoup(resp.text, 'html.parser')

    brands_urls = []

    brands = resp.find('div',class_='dropdown-menu dropdown-menu-w100')
    brands = brands.find_all("a" , gacatagory="Header" )

    for i in range(len(brands)): 
        brands_tamp = []
        brands_tamp.append(brands[i].text)
        brands_tamp.append(brands[i].get('href'))
        brands_urls.append(brands_tamp)
        
    brands_urls = brands_urls[:-1]
        
    return brands_urls

def Get_brands_products (query_url , brands_urls):    
    headers = {'User-Agent': USER_AGENT_VALUE }
    
    products_urls = []
    
    for j in range(len(brands_urls[:])):
        resp = requests.get(query_url + brands_urls[j][1], headers=headers)
        
        resp.encoding = 'UTF-8'
        resp = BeautifulSoup(resp.text, 'html.parser')
        
        products_hot = resp.find_all("div" , class_='mix-item col-12 col-lg-4 cat2 price4 fcellphone' )
        products = resp.find_all("div" , class_='mix-item col-6 col-sm-3 col-lg-2 cat2 price4 fcellphone' )
        products = products_hot+products
        
        for i in range(len(products)): 
            onsale_product = []
            onsale_product.append(j)
            products_top = products[i].find('span',class_="badge badge-danger pos-a-lt ml-3 mt-3")
            if products_top != None:
                onsale_product.append(products[i].find("a" , class_="text-row-1" , gacatagory="品牌頁_已上市" ).text)
                if products[i].find('a',class_="text-price h6" , gacatagory="品牌頁_已上市") == None:
                    onsale_product.append(products[i].find('strong',class_="text-price h6" ).text)
                else : 
                    onsale_product.append(products[i].find('a',class_="text-price h6" , gacatagory="品牌頁_已上市").text)
                onsale_product.append(products[i].find("a" , class_="text-row-1" , gacatagory="品牌頁_已上市").get('href'))
            elif products[i].find("a" , class_="text-row-2" , gacatagory="品牌頁_已上市") == None:
                break
            else :
                onsale_product.append(products[i].find("a" , class_="text-row-2" , gacatagory="品牌頁_已上市").text)
                if products[i].find('a',class_="text-price h6" , gacatagory="品牌頁_已上市") == None:
                    onsale_product.append(products[i].find('strong',class_="text-price h6" ).text)
                else:
                    onsale_product.append(products[i].find('a',class_="text-price h6" , gacatagory="品牌頁_已上市").text)
                onsale_product.append(products[i].find("a" , class_="text-row-2" , gacatagory="品牌頁_已上市").get('href'))
            products_urls.append(onsale_product)
            
    return products_urls

def Get_brands_p_detial (query_url , products_urls):
    headers = {'User-Agent': USER_AGENT_VALUE }
    
    p_detials_list = []
    
    for product in products_urls[:]:

        resp = requests.get(query_url + product[3], headers=headers)
        resp.encoding = 'UTF-8'
        resp = BeautifulSoup(resp.text, 'html.parser')
        
        product_detials = resp.find('table', class_="table table-bordered")
        
        detial_name = product_detials.find_all('th', class_="active")
        detial_content = product_detials.find_all('td')
        
        detial_name_list= []
        detial_content_list = []
        for i in range(len(detial_name)):
            detial_name_list.append(detial_name[i].text)
            detial_content_list.append(detial_content[i].text)

        p_detial_temp = zip(detial_name_list,detial_content_list)
        p_detials_list.append(dict(p_detial_temp))
    
    return p_detials_list


search_brands = Get_brands_url(USER_AGENT_VALUE , query_url , page_url)
search_product = Get_brands_products(query_url , search_brands)
search_detial = Get_brands_p_detial(query_url,search_product)

detial_temp = copy.deepcopy(search_detial[0])

for j in search_detial[1:]:
    temp = list(j)
    for i in range(len(j)):
        if detial_temp.get(temp[i],"None") == 'None':
            detial_temp[temp[i]] = j[temp[i]]

item = list(detial_temp.keys())


csv_detial = []
for i in range(len(search_detial)):
    csv_temp = []
    #csv_temp.append(search_product[i][1])
    for j in  range(len(item[1:])):

        if search_detial[i].get(item[j],"None") == 'None':
            csv_temp.append('')
        else :
            csv_temp.append(search_detial[i][item[j]])
    csv_detial.append(csv_temp)
           
item.insert(0 , '產品')
for i in range(len(search_product)):
    csv_detial[i].insert(0,search_product[i][1])

#---------------------------------------

with open('./cellphone2.csv', 'w' , newline='' , encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    
    writer.writerow(item)
    
    for i in range(len(csv_detial)):
        writer.writerow(csv_detial[i])

end = time.time() 
print(end-start)
