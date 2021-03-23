# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 09:01:27 2021

@author: Petzi
"""

import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow
from collections import defaultdict
import re
import pprint
import pandas as pd

import add_help_functions as helper
wiki_path = 'https://de.wikipedia.org/wiki/Verwaltungsgliederung_Berlins#Bezirke'
berlin_dict = helper.get_berlin_district_names(wiki_path)

#OSMFILE = "Berlin_OSM_v2_k20.osm"
OSMFILE = "Berlin_OSM_v2.osm"

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["straße", "strasse", "platz", "weg", "allee", "damm", "ufer", "gasse"]

############################################################################
                           
def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_cuisine(elem):
    return (elem.attrib['k'] == "cuisine")

def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def is_addr_city(elem):
    return (elem.attrib['k'] == "addr:city")

def is_addr_country(elem):
    return (elem.attrib['k'] == "addr:country")

def is_country(elem):
    return (elem.attrib['k'] == "country")

def is_suburb(elem):
    return (elem.attrib['k'] == "addr:suburb")

def audit_value(value_dict, value):
    value_dict.setdefault(value,0)
    value_dict[value]+=1

def audit_value_cuisine(value_dict, value):
    
    value_list = value.split(";")
    value_list = [i.strip() for i in value_list]
    for value in value_list:
        value_dict.setdefault(value,0)
        value_dict[value]+=1   

def audit_value_suburb(value_dict, value):
     
    value_dict.setdefault(value,0)
    value_dict[value]+=1

    if value not in berlin_dict.keys():
        value_dict.setdefault("Not a Bourough!",0)
        value_dict["Not a Bourough!"]+=1

def audit_street_type(street_types, street_name):
    
    x=0    
    for expected_street_type in expected:
        if expected_street_type in street_name.lower():
            x=1
            break
            
    if x==0:
        street_types[street_name].add(street_name)
############################################################################

def audit(osm_file):
    street_types = defaultdict(set)
    postcode = {}
    cuisine={}
    suburb={}
    city = {}
    addr_country={}
    country={}
    
    for event, elem in ET.iterparse(osm_file, events=("end",)):

        if elem.tag == "node" or elem.tag == "way":

            for child in elem.iter("tag"):
                
                if is_street_name(child):
                    audit_street_type(street_types, child.attrib['v'])
                
                elif is_postcode(child):
                     audit_value(postcode, child.attrib['v'])
                
                elif is_cuisine(child):
                     audit_value_cuisine(cuisine, child.attrib['v'])                    
                
                elif is_suburb(child):
                    audit_value_suburb(suburb, child.attrib['v']) 
                
                elif is_addr_city(child):
                    audit_value(city, child.attrib['v'])  
                
                elif is_addr_country(child):
                    audit_value(addr_country, child.attrib['v'])  

                elif is_country(child):
                    audit_value(country, child.attrib['v']) 
            
    return (street_types, postcode, cuisine, suburb, city, addr_country, country)

def test():
    st_types    = audit(OSMFILE)[0]
    postcode    = audit(OSMFILE)[1]
    cuisine     = audit(OSMFILE)[2]
    suburb      = audit(OSMFILE)[3]
    city        = audit(OSMFILE)[4]
    addr_country= audit(OSMFILE)[5]
    country     = audit(OSMFILE)[6]
    
    pprint.pprint(dict(st_types))
    pprint.pprint(dict(postcode))
    #pprint.pprint(dict(cuisine))
    pprint.pprint(dict(suburb))
    pprint.pprint(dict(city))
    pprint.pprint(dict(addr_country))
    pprint.pprint(dict(country))
    
    #print (sum(suburb.values()))
    df = pd.DataFrame(list(suburb.items()),columns = ['Borough','Count'])
    print (df)

if __name__ == '__main__':
    test()
    


