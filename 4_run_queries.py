# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import add_help_functions as helper
wiki_path = 'https://de.wikipedia.org/wiki/Verwaltungsgliederung_Berlins#Bezirke'
berlin_dict = helper.get_berlin_district_names(wiki_path)

import sqlite3
import pandas as pd
import os
import pprint

path		= os.getcwd()
db_name = "berlin_osm.db"
db_path = os.path.join(path,db_name)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

query_postcode = """ 
SELECT value,
       count( * ) AS count
  FROM (
           SELECT *
             FROM nodes_tags
           UNION ALL
           SELECT *
             FROM ways_tags
       )
 WHERE [key] = "postcode"
 GROUP BY value
 ORDER BY count DESC
 LIMIT 10
""" 

query_cuisine = """ 
SELECT value,
       count( * ) AS count
  FROM (
           SELECT *
             FROM nodes_tags
           UNION ALL
           SELECT *
             FROM ways_tags
       )
 WHERE [key] = "cuisine"
 GROUP BY value
 ORDER BY count DESC
 limit 10
 """ 

query_nodes = """ 
SELECT count( * ) AS count
  FROM nodes;
 """
 
query_ways = """ 
SELECT count( * ) AS count
  FROM ways;
 """ 

query_top_user = """ 
SELECT user,
       count( * ) AS count
  FROM (
           SELECT user
             FROM nodes
           UNION ALL
           SELECT user
             FROM ways
       )
 GROUP BY user
 ORDER BY count DESC
 LIMIT 10
 """ 
query_user = """ 
SELECT count( * ) 
  FROM (
           SELECT user,
                  count( * ) AS count
             FROM (
                      SELECT user
                        FROM nodes
                      UNION ALL
                      SELECT user
                        FROM ways
                  )
            GROUP BY user
            ORDER BY count DESC
       );
 """ 
query_suburb = """ 
SELECT value,
       count( * ) AS count
  FROM (
           SELECT *
             FROM nodes_tags
           UNION ALL
           SELECT *
             FROM ways_tags
       )
 WHERE [key] = "suburb"
 GROUP BY value
 ORDER BY count DESC;
 """ 

query_addr = """ 
SELECT [key],
       count( * ) AS count
  FROM (
           SELECT *
             FROM nodes_tags
           UNION ALL
           SELECT *
             FROM ways_tags
       )
 WHERE type = "addr"
 GROUP BY [key]
 ORDER BY count DESC
 LIMIT 6;
 """ 
query_tree = """ 
SELECT count( * ) AS count
  FROM nodes_tags
 WHERE value = "tree";
 """

query_amenity = """ 
SELECT value,
       count( * ) AS count
  FROM (
           SELECT *
             FROM nodes_tags
           UNION ALL
           SELECT *
             FROM ways_tags
       )
 WHERE [key] = "amenity"
 GROUP BY value
 ORDER BY count DESC
 limit 10
 """ 

query_dict ={"postcode":    ["query_postcode.csv",  query_postcode, ['postcode', 'count']],
             "cuisine":     ["query_cuisine.csv",   query_cuisine,  ['cuisine', 'count']],
             "nodes":       ["query_nodes.csv",     query_nodes,    ['Node Count']],
             "ways":        ["query_ways.csv",      query_ways,     ['Way Count']],
             "top_user":    ["query_top_user.csv",  query_top_user, ['top user', 'count']],
             "user":        ["query_user.csv",      query_user,     ['user Count']],
             "suburb":      ["query_suburb.csv",    query_suburb,   ['suburb', 'count']],
             "address":     ["query_addr.csv",    query_addr,   ['addr key', 'count']],
             "tree":        ["query_tree.csv",    query_tree,   ['Tree Count']],
             "amenity":     ["query_amenity.csv",    query_amenity,   ['amenity', 'count']],}

if __name__ == '__main__':
    conn_db = create_connection(db_path)
    cursor = conn_db.cursor()
    
    for query in query_dict:
        
        query_sql = query_dict[query][1]
        cursor.execute(query_sql)
        results = cursor.fetchall()
        
        print (query_sql)
        
        df = pd.DataFrame(results)
        df.columns = query_dict[query][2]
        
        print(df)
        
        dirName="query_results"
        
        if not os.path.exists(dirName):
            os.mkdir(dirName)
            
        result_file = query_dict[query][0]
        
        result_path = os.path.join(path,dirName,result_file)
        df.to_csv(result_path,index=False, header=True)     

conn_db.close()

