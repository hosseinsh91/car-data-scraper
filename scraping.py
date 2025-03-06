import requests 
from bs4 import BeautifulSoup 
import re 
import mysql.connector
from collections import OrderedDict
cnx = mysql.connector.connect(user='',password='',
                              host='',
                              database='')
mycursor = cnx.cursor()
car=str(input('Enter Your TABLE name: '))
mycursor.execute("CREATE TABLE %s (Car_Name VARCHAR(300), Price VARCHAR(300) , Used varchar(300) , Count INT(200))" % car)
Car_name=str(input('Enter your Car name: ')) 
url = 'https://ae.opensooq.com/en/post/search'
query = {'term': Car_name} 
urllink = requests.get(url, params=query) 
soup =BeautifulSoup(urllink.text, 'html.parser')
page=soup.find_all('div',attrs={'class':'rectLiDetails tableCell vMiddle pr15'})
basic_info = []
for item in page:
    basic_info.append(item)
prices=soup.find_all('span',attrs={'class':'inline ltr'})
costs=[]
for price in prices:
    costs.append(re.sub('\s+' , ' ' , price.text).strip())
kms=[]
for km in basic_info :
    kms.append(km.find_all("li", attrs = {'class':'ml8'})[0].findNext('li').findNext('li').findNext('li').text.strip())
used=[]
for km in kms :
    key=re.sub('\s+' , ' ' , km).strip()
    if re.search(r'^[0-9,\]+[\s-]+[0-9,]*$', key )!=None:
        used.append(key)
    else:
        used.append('None')
dic=OrderedDict()
dic = OrderedDict(zip(costs, used))
cursor= cnx.cursor()
counter=1
for item in list(dic.keys()) :
    if dic[item]!='None':
        cursor.execute(' INSERT INTO %s VALUES  (\'%s\' , \'%s\' , \'%s\' , %i )' % (car ,Car_name , item , dic[item] , counter))
    counter+=1
    if counter==21:
        break
    
cnx.commit()
cnx.close()

