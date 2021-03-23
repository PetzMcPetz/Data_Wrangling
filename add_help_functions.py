# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 14:01:34 2021

@author: Petzi
"""

from bs4 import BeautifulSoup
import requests
import pprint

wiki_path = 'https://de.wikipedia.org/wiki/Verwaltungsgliederung_Berlins#Bezirke'

def get_berlin_district_names(html_in):
    
    store_dict={}
    
    s=requests.Session()
    r=s.get(html_in)
    soup = BeautifulSoup(r.text,features="lxml")
    
    tbody_list = soup.find_all('table')
    
    tbody = tbody_list[1] # Second table on webpage to be used
    
    tr_list = tbody.find_all('tr')
    
    for tr in tr_list:
    
        a_list = tr.find_all('a')     
        
        try:
            
            disctrict = a_list[0].string.strip()
            borough = a_list[1].string.strip()

            store_dict.setdefault(borough,[])
            store_dict[borough].append(disctrict)

        except:
            continue

    return store_dict


#wiki_path ="https://wiki.openstreetmap.org/wiki/DE:Key:cuisine"


def get_cuisine_values(html_in):
    ''' Not used
    '''
    store_dict={}

    s=requests.Session()
    r=s.get(html_in)
    soup = BeautifulSoup(r.text,features="lxml")
    
    tbody_list = soup.find_all('table')
      
    tbody = tbody_list[2] # Third table on webpage to be used
        
    tr_list = tbody.find_all('tr')
        
    for tr in tr_list:
        
        a_list = tr.find_all('a')     
            
        try:
                
            column_1 = a_list[0].string.strip()
            column_2 = a_list[1].string.strip()

            store_dict.setdefault(column_1,[])
            store_dict[column_1].append(column_2)
    
        except:
            continue
    
    return (store_dict)


def reverse_dict(org_dict):
    
    mod_dict={}
    
    for key in org_dict:
        mod_dict.setdefault(key,key)
        for item in org_dict[key]:
            mod_dict.setdefault(item,key)
    
    return  mod_dict 


def reverse_dict_v2(org_dict):
    
    mod_dict={}
    
    for key in org_dict:
        #mod_dict.setdefault(key,key)
        for item in org_dict[key]:
            mod_dict.setdefault(item,key)
    
    return  mod_dict 

