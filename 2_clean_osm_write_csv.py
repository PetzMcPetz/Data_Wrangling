#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 23:03:59 2021

@author: Michael Rabe
"""

import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow
from collections import defaultdict
import re
import pprint
import csv
import codecs

import cerberus

import add_help_functions as helper
wiki_path = 'https://de.wikipedia.org/wiki/Verwaltungsgliederung_Berlins#Bezirke'
berlin_dict = helper.get_berlin_district_names(wiki_path)
berlin_dict = helper.reverse_dict(berlin_dict)


#wiki_path ="https://wiki.openstreetmap.org/wiki/DE:Key:cuisine"
#cuisine_dict = helper.get_cuisine_values(wiki_path)
#cuisine_dict = helper.reverse_dict_v2(cuisine_dict)

import add_schema
osm_schema = add_schema.get_schema()

#OSMFILE = "Berlin_OSM_v2_k20.osm"
OSMFILE = "Berlin_OSM_v2.osm"

lower_colon     = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
problemchars    = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

NODES_PATH      = "nodes.csv"
NODE_TAGS_PATH  = "nodes_tags.csv"
WAYS_PATH       = "ways.csv"
WAY_NODES_PATH  = "ways_nodes.csv"
WAY_TAGS_PATH   = "ways_tags.csv"

NODE_FIELDS         = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS    = ['id', 'key', 'value', 'type']
WAY_FIELDS          = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS     = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS    = ['id', 'node_id', 'position']

###############################################################################

def get_type_and_key(entry):
    
    entry_type = 'regular'
    entry_key = entry
    
    temp_list = entry_key.split(":")
    if len(temp_list)>1:
        entry_type = temp_list[0]
        entry_key = ":".join(temp_list[1:])    

    return (entry_type, entry_key)

###############################################################################

def is_suburb_name(elem):
    return (elem.attrib['k'] == "addr:suburb")

def upd_suburb(inp_dict, value):
    ''' function to harmonize "addr:suburb" values
    :param inp_dict: reversed berlin dictionary extracted from wiki
    :param value: is the "addr:suburb" value
    '''
    try:
        value = inp_dict[value]
    except:
        print ("value not found:",value)
    
    return value

###############################################################################

cuisine_mapping = { "coffee_shop": ["coffee"],
           "barbecue":['bbq'],
           "arab":["arabic"],
           "israeli":['isreali'],
           "italian":['italian_pizza'],
           "burrito":['burritos']
            }     

cuisine_dict = helper.reverse_dict_v2(cuisine_mapping)

def is_cuisine(elem):
    return (elem.attrib['k'] == "cuisine")

def upd_cuisine(inp_dict, value):
    ''' function to harmonize "cusine" values
    :param inp_dict: cuisine_dict > reversed cuisine_mapping dict
    :param value: is the "cuisine" value
    Step1: Split value in a list by semicolon
    Step2: Loop trough the list and correct the value if necessary
    Step3: Check if corrected value already in the list. If yes drop the list index.
    '''
    
    value_list = value.split(";") # Step 1
    value_list = [i.strip() for i in value_list]
    
    for i in range(0,len(value_list)):
        
        entry = value_list[i]
        
        if entry in inp_dict.keys():# Step2
           
            new_entry = inp_dict[entry]
            
            if new_entry not in value_list: #Step3
                value_list[i] = new_entry
            else:
                value_list.pop(i)
            
    return value_list

###############################################################################

def shape_element(element):
    
    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []
    
    store_dict={}
    
    format_list_int = ['id', 'changeset', 'uid']
    format_list_float = ['lat', 'lon']
        
    for key in element.attrib.keys():
            
        if key in format_list_int:
            store_dict[key]=int(element.attrib[key])
        elif key in format_list_float:
            store_dict[key]=float(element.attrib[key])
        else:
            store_dict[key]=str(element.attrib[key])
    
    counter = 0   
    
    for child in element:
        
        if child.tag == "tag":
            
            entry_key = child.attrib['k']
            entry_value = child.attrib['v']
            
            if problemchars.search(entry_key):
                print (entry_value, "found")
                continue
            
            entry_type, entry_key = get_type_and_key(entry_key)
            
            if is_suburb_name(child):
                entry_value = upd_suburb(berlin_dict, entry_value)            
                
            loop_list=[entry_value]
            
            if is_cuisine(child):
                loop_list = upd_cuisine(cuisine_dict, entry_value)                  
                
            for entry_value in loop_list:
                
                tags.append({"id": store_dict['id'],
                            "key": entry_key,
                            "value":entry_value ,
                            "type":entry_type})
        
        elif child.tag == "nd":
            
            node_id = int(child.attrib['ref'])
            
            way_nodes.append({'id': store_dict['id'],
                              'node_id': node_id,
                              'position': counter})
            counter+=1        

    if element.tag == 'node':
        node_attribs = store_dict
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        way_attribs=store_dict
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

###############################################################################

def validate_element(element, validator, schema=osm_schema):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))

###############################################################################

def process_map(osm_file, validate):

    with codecs.open(NODES_PATH, 'w',encoding='utf-8') as nodes_file, \
         codecs.open(NODE_TAGS_PATH, 'w',encoding='utf-8') as nodes_tags_file, \
         codecs.open(WAYS_PATH, 'w',encoding='utf-8') as ways_file, \
         codecs.open(WAY_NODES_PATH, 'w',encoding='utf-8') as way_nodes_file, \
         codecs.open(WAY_TAGS_PATH, 'w',encoding='utf-8') as way_tags_file:       
        
        nodes_writer        = csv.DictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer    = csv.DictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer         = csv.DictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer    = csv.DictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer     = csv.DictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        elem_list=["node","way"]
    
        validator = cerberus.Validator()
        
        for event, element in ET.iterparse(osm_file, events=("end",)):
            
            if element.tag in elem_list:
                el = shape_element(element)
                if el:
                    if validate is True:
                        None
                        validate_element(el, validator)
     
                    if element.tag == 'node':
                        nodes_writer.writerow(el['node'])
                        node_tags_writer.writerows(el['node_tags'])
                    elif element.tag == 'way':
                        ways_writer.writerow(el['way'])
                        way_nodes_writer.writerows(el['way_nodes'])
                        way_tags_writer.writerows(el['way_tags'])        


if __name__ == '__main__':
    #test()
    process_map(OSMFILE, validate=True)