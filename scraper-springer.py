# -*- coding: utf-8 -*-

import slate3k as slate
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import wget

ruta_descarga = '/home/user/springer-books/'
with open('/home/user/springer-books/Springer Ebooks.pdf', 'rb') as f:
    links_springer = slate.PDF(f)
    
list_links = []


for l in links_springer:
    aux = l.split('\n\n')
    for a in aux:
        if 'http://' in a:
            list_links.append(a)
        else:
            pass
        
data = pd.DataFrame(columns = ['title','authors','original_link','link_download'])

for l in range(len(list_links)):
    try:
        soup = BeautifulSoup(requests.get(list_links[l]).text)

        title = soup.find('div',{'class':'page-title'}).text.replace('\n','')
        authors = ','.join([s.text.replace('\xa0',' ') for s in soup.find_all('span',{'class':'authors__name'})])
        link_download = 'https://link.springer.com'+soup.find('div',{'class':'cta-button-container__item'}).find('a')['href']
        wget.download(link_download, ruta_descarga + title +'.pdf')
        
        row = {'title':title,'authors':authors,'original_link':list_links[l],'link_download':link_download}
        data = data.append(row, ignore_index = True)
    
    except:
        print('Link fallido: '+list_links[l])
        pass
    print('iteración '+str(l+1)+' de '+str(len(list_links)))
    time.sleep(2)
    
data.to_excel(ruta_descarga+'summary.xlsx', index = False)