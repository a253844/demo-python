# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 22:21:03 2020

@author: USER
"""
from bs4 import BeautifulSoup
import time

from selenium import webdriver
import pymysql

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')

while True:
	db = pymysql.connect(host="",
					 user="root", 
					 passwd="", 
					 db="dbtest")
	cursor = db.cursor()

	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.get("https://www.twreporter.org/i/covid-2019-keep-tracking-gcs")
	time.sleep(5)
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	driver.close()
	driver.quit()

	region_data = soup.find_all('td',class_='table__TD-sc-1ji413w-0 idjyyX')

	all_data = []
	for i in range(0,len(region_data),3):
		data = []
		data.append(region_data[i].text)
		data.append((region_data[i+1].text).replace(',' , ''))
		data.append((region_data[i+2].text).replace(',' , ''))
		all_data.append(data)

	cursor.execute("SELECT N_ID , N_CH_Name , N_EN_Name  FROM nation ")

	dbdata=[item for item in cursor.fetchall()]

	db_dict_CH = {}
	db_dict_EN = {}
	for i in range(len(dbdata)):
		db_dict_CH[dbdata[i][1]]=dbdata[i][0]
		db_dict_EN[dbdata[i][2]]=dbdata[i][0]

	today = time.strftime("%Y/%m/%d", time.localtime())
	insert_data = "insert into infect (I_N_ID , I_Infect,I_Death , date) value"
	updata_data = "update infect set"

	db_list =[]
	db_id = []
	for i in range(len(all_data)):
		try:
			getid = db_dict_CH[all_data[i][0]]
			cursor.execute("SELECT I_N_ID, I_Infect , I_Death  FROM infect where I_N_ID =" + str(getid) +"" )
			dbnationdata=[item for item in cursor.fetchall()]
			db_list.append(dbnationdata)
			db_id.append(getid)
		except:
			db_list.append([])
			db_id.append([])
			continue
	   
	for i in range(len(db_list)):
		if db_list[i] != []:
			if int(db_list[i][0][1]) < int(all_data[i][1]) or int(db_list[i][0][2]) < int(all_data[i][2]):
			   updata =  " I_Infect = '"+str(all_data[i][1])+ "', I_Death = '" +str(all_data[i][2])+ "' , date = '" +today+ "' where (I_N_ID ='" +str(db_list[i][0][0])+ "')"
			   cursor.execute(updata_data+updata)
			   db.commit()
			   print("updata : "+ updata)
		elif db_id[i] != [] :
			insert = "('" + str(db_id[i]) + "','" + str(all_data[i][1]) + "','" + str(all_data[i][2]) + "','" + today + "')" 
			cursor.execute(insert_data+insert)
			db.commit()
			print("insert data : " + insert)

	cursor.close()
	db.close()
	print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
	time.sleep(600)