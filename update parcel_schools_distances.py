# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 21:54:25 2021

@author: lehrs
"""

import psycopg2
import re
import matplotlib.pyplot as plt
import os
import pandas as pd

# connection to database:
try:
    conn = psycopg2.connect("dbname='spatial' user='postgres' host='localhost' password='220650'")
except:
    print("cant connect to the database")

cur = conn.cursor()
cur2 = conn.cursor()
cur3 = conn.cursor()
input_altkey = 3565215



sql = "select parid::integer from volusia.parcel p where geom is not null" # limit 10"

print('SQL: ', sql)
cur.execute(sql)

# one way grab all the data into a multi-dimensional array
#data = cur.fetchall()
#actual_data = data[0][0]

# I like to fetch one row at a time like reading data from a file
i=0
row = cur.fetchone()
while row is not None:
    i = i + 1
    parid = str(row[0])
    sql2 = "select p.parid::integer, p.geom, ST_Distance(p.geom, (select p2.geom from volusia.parcel p2 where p2.parid=" + parid + "))/5280  from volusia.parcel p where p.luc='8300' order by p.geom <-> (select p2.geom from volusia.parcel p2 where p2.parid=" + parid + ") limit 1;"
    cur2.execute(sql2)
    row2 = cur2.fetchone()
    parid2 = str(row2[0])
    distance = row2[2]
    sql3 = "update volusia.parcel p1 set scdistance = " + str(distance) + " where p1.parid=" + parid + ";"
    cur3.execute(sql3)
    # print(sql3)
    if i%10000 == 0:
        print(i)
        conn.commit()
    row = cur.fetchone()

#df = pd.
conn.commit()
conn.close()


