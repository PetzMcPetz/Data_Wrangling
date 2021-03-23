# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 10:18:19 2021

@author: Petzi
"""

import sqlite3
from sqlite3 import Error
from sqlalchemy import create_engine
import pandas as pd
import os

path	= os.getcwd()
db_name = "berlin_osm.db"
db_path = os.path.join(path,db_name)

def create_database(db_file):
    """ taken from https://www.sqlitetutorial.net/sqlite-python/creating-database/"""
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        print ("Database created")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            

def create_connection(db_file):
    """ taken from https://www.sqlitetutorial.net/sqlite-python/creating-database/"""
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


def create_table(conn, create_table_sql):
    """ taken from https://www.sqlitetutorial.net/sqlite-python/creating-database/"""
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def import_csv(infile, table, conn_db):
    """ import a csv file into SQL db table
    :param infile: csv file including header
    :param table: SQL table
    :param conn_db : SQL database
    :return None
    """
    df = pd.read_csv(infile)
    df.to_sql(table, con=conn_db,if_exists='append', index=False)

sql_create_nodes_table = """ CREATE TABLE nodes (
                                id INTEGER PRIMARY KEY NOT NULL,
                                lat REAL,
                                lon REAL,
                                user TEXT,
                                uid INTEGER,
                                version TEXT,
                                changeset INTEGER,
                                timestamp TEXT
                                ); """

sql_create_nodes_tags_table = """ CREATE TABLE nodes_tags (
                                id INTEGER,
                                key TEXT,
                                value TEXT,
                                type TEXT,
                                FOREIGN KEY (id) REFERENCES nodes(id)
                                ); """

sql_create_ways_table = """ CREATE TABLE ways (
                                id INTEGER PRIMARY KEY NOT NULL,
                                user TEXT,
                                uid INTEGER,
                                version TEXT,
                                changeset INTEGER,
                                timestamp TEXT
                                ); """

sql_create_ways_tags_table = """ CREATE TABLE ways_tags (
                                id INTEGER NOT NULL,
                                key TEXT NOT NULL,
                                value TEXT NOT NULL,
                                type TEXT,
                                FOREIGN KEY (id) REFERENCES ways(id)
                                ); """

sql_create_ways_nodes_table = """ CREATE TABLE ways_nodes (
                                id INTEGER NOT NULL,
                                node_id INTEGER NOT NULL,
                                position INTEGER NOT NULL,
                                FOREIGN KEY (id) REFERENCES ways(id),
                                FOREIGN KEY (node_id) REFERENCES nodes(id)
                                ); """

input_dict ={"nodes":       ["nodes.csv",       sql_create_nodes_table],
             "nodes_tags":  ["nodes_tags.csv",  sql_create_nodes_tags_table],
             "ways":        ["ways.csv",        sql_create_ways_table],
             "ways_nodes":  ["ways_nodes.csv",  sql_create_ways_nodes_table],
             "ways_tags":   ["ways_tags.csv",   sql_create_ways_tags_table]}

if __name__ == '__main__':
    create_database(db_path)
    conn_db = create_connection(db_path)
    
    for table in input_dict:
        print (table)
        sql_table_cmd = input_dict[table][1]
        sql_input_file = input_dict[table][0]
        
        create_table(conn_db,sql_table_cmd)
        import_csv(sql_input_file, table, conn_db)
        
    conn_db.close()