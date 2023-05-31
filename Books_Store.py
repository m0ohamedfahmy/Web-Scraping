import requests
from bs4 import BeautifulSoup
import csv
import pandas
soup=BeautifulSoup(requests.get('http://books.toscrape.com/catalogue/category/books/travel_2/index.html').text,'html.parser')
with open('books.csv','w',encoding='utf-8',newline='') as t:
            writer=csv.writer(t)
            writer.writerow(['Book_name','Rate','Price','Category'])


soup=BeautifulSoup(requests.get('http://books.toscrape.com/catalogue/category/books_1/index.html').text,'html.parser')
url=[]
row=[]
row_0=[]
rate={'One':1,'Two':2,'Three':3,'Four':4,'Five':5}

for i in soup.find_all('ul',attrs={'class':"nav nav-list"}):
        for l in i.find_all('a'):
            if l.get('href').replace('..','http://books.toscrape.com/catalogue/category')=='index.html':
                continue
            else:
                url.append(l.get('href').replace('..','http://books.toscrape.com/catalogue/category'))
for link in url:                    
    soup=BeautifulSoup(requests.get(link).text,'html.parser')
    if soup.find('li',attrs={'class':'next'})==None:
        with open('books.csv','a',encoding='utf-8',newline='') as th:
            writer=csv.writer(th)
            for travel in soup.find_all('article',attrs={'class':'product_pod'}):
                row_0.append(travel.find('h3').find('a').get('title'))
                row_0.append(rate[travel.find('p',attrs={'class':'star-rating'}).get('class')[1]])
                row_0.append(travel.find('p',attrs={'class':'price_color'}).get_text()[2:])
                row_0.append(soup.find('h1').get_text())
                writer.writerow(row_0)
                row_0=[]
                print('no_next')
    elif soup.find('li',attrs={'class':'next'})!=None:
        Num=1
        while True:
            soup=BeautifulSoup(requests.get(link.replace('index',f'page-{Num}')).text,'html.parser')
            with open('books.csv','a',encoding='utf-8',newline='') as m:
                writer=csv.writer(m)
                for my in soup.find_all('article',attrs={'class':'product_pod'}):
                    row.append(my.find('h3').find('a').get('title'))
                    row.append(rate[my.find('p',attrs={'class':'star-rating'}).get('class')[1]])
                    row.append(my.find('p',attrs={'class':'price_color'}).get_text()[2:])
                    row.append(soup.find('h1').get_text())
                    writer.writerow(row)
                    row=[]
            if soup.find('li',attrs={'class':'next'}):
                Num+=1
            else:
                print('finished')
                break
df=pandas.read_csv('books.csv')
print(df)
