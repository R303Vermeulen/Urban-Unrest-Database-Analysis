import mysql.connector
from mysql.connector import Error

import matplotlib
from matplotlib import pyplot as plt

import pygal
from pygal.style import Style
import pygal_maps_world as pa

pwdfileName = 'pss'
pwdfile = open("account.info.txt", 'r')
lines = pwdfile.readlines()
u = lines[0][:-1]
p = lines[1][:-1]


hostName = 'mysql.labthreesixfive.com'
portName = '3306'
userName = u
passString = p

dbName = 'LAB8'

try:

    conn = mysql.connector.connect(host=hostName, port=portName, database=dbName,
                                   user=userName, password=passString)
    if conn.is_connected():
        print('Connected to ', hostName)

        cursor = conn.cursor()

        cursor.execute("(WITH \n"
                       "maxds AS ( SELECT CASE \n"
                       "WHEN maxDeaths = -1 THEN minDeaths \n"
                       "WHEN maxDeaths > -1 THEN maxDeaths \n"
                       "END as maxd, Ptype, City \n"
                       "FROM Events \n"
                       "WHERE deathFlag = 1 ), \n"
                       "conts AS ( SELECT co.Country, SUM(m.maxd) as deathTot \n"
                       "FROM Countries co, Cities ci, maxds m \n"
                       "WHERE co.ISO3 = ci.Country and \n"
                       "ci.CityId = m.City \n"
                       "GROUP BY co.ISO3, co.Country ), \n"
                       "maxdeathc AS ( SELECT MAX(deathTot) as mdc\n"
                       "FROM conts ), \n"
                       "maxc AS ( SELECT c.Country \n"
                       "FROM conts c, maxdeathc m \n"
                       "WHERE c.deathTot = m.mdc ), \n"
                       "dperes AS ( SELECT md.Ptype, SUM(maxd)/COUNT(*) as dpere \n"
                       "FROM maxds md, Countries co, Cities ci, maxc mc, ProblemTypes p \n"
                       "WHERE co.ISO3 = ci.Country and \n"
                       "ci.CityId = md.City and \n"
                       "(co.Country != mc.Country or \n"
                       "(md.Ptype = p.Ptype and \n"
                       "p.ProblemType != 'Armed Battle/Clash')) \n"
                       "GROUP BY md.Ptype )\n"
                       "SELECT p.ProblemType, d.dpere \n"
                       "FROM ProblemTypes p, dperes d \n"
                       "WHERE p.Ptype = d.Ptype \n"
                       "ORDER BY d.dpere DESC) \n"
                       "UNION \n"
                       "(WITH \n"
                       "maxds AS ( SELECT CASE \n"
                       "WHEN maxDeaths = -1 THEN minDeaths \n"
                       "WHEN maxDeaths > -1 THEN maxDeaths \n"
                       "END as maxd, Ptype, City \n"
                       "FROM Events \n"
                       "WHERE deathFlag = 1 ), \n"
                       "conts AS ( SELECT co.Country, SUM(m.maxd) as deathTot \n"
                       "FROM Countries co, Cities ci, maxds m \n"
                       "WHERE co.ISO3 = ci.Country and \n"
                       "ci.CityId = m.City \n"
                       "GROUP BY co.ISO3, co.Country ), \n"
                       "maxdeathc AS ( SELECT MAX(deathTot) as mdc\n"
                       "FROM conts ), \n"
                       "maxc AS ( SELECT c.Country \n"
                       "FROM conts c, maxdeathc m \n"
                       "WHERE c.deathTot = m.mdc ), \n"
                       "dperes AS ( SELECT md.Ptype, SUM(md.maxd)/COUNT(*) as dpere \n"
                       "FROM maxds md, Countries co, Cities ci, maxc mc, ProblemTypes p \n"
                       "WHERE co.ISO3 = ci.Country and \n"
                       "ci.CityId = md.City and \n"
                       "co.Country = mc.Country and \n"
                       "md.Ptype = p.Ptype and \n"
                       "md.maxd > 10000 and \n"
                       "p.ProblemType = 'Armed Battle/Clash' \n"
                       "GROUP BY md.Ptype ) \n"
                       "SELECT p.ProblemType, d.dpere \n"
                       "FROM ProblemTypes p, dperes d \n"
                       "WHERE p.Ptype = d.Ptype) \n"
                       "ORDER BY dpere DESC ;")

        records = cursor.fetchall()
        pyth1 = records

        # print("---------------------------------------")
        # for r in records:
        #   print(r)
        # print("---------------------------------------")


except Error as e:
    print('Connection error: ', e)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print('Done')

####################### now to process the query into a bar chart

l = len(pyth1)

newp = []
for i in range(l):
    newp.append([])
    newp[i].append(pyth1[i][0])
    newp[i].append(int(pyth1[i][1]))

newp[0][0] = 'Rwanda genocide of 1994'

ptypes = []
values = []
for i in range(l):
    ptypes.append(newp[i][0])
    values.append(newp[i][1])

fig = plt.figure(figsize=(10, 5))

# creating the bar plot
plt.barh(ptypes, width=values)

plt.xlabel("Deaths per event of each Problem Type")
plt.ylabel("Problem Types")
plt.title(
    "Deaths per event of each Problem Type & the Rwanda genocide of 1994 - (Armed Battle/Clash does not include events from the Randa genocide of 1994)")
plt.show()

###################second bar graph
newp = []
for i in range(l):
    if i != 0:
        newp.append([])
        newp[i - 1].append(pyth1[i][0])
        newp[i - 1].append(int(pyth1[i][1]))

ptypes = []
values = []
for i in range(l - 1):
    ptypes.append(newp[i][0])
    values.append(newp[i][1])

fig = plt.figure(figsize=(10, 5))

# creating the bar plot
plt.barh(ptypes, width=values)

plt.xlabel("Deaths per event of each Problem Type")
plt.ylabel("Problem Types")
plt.title(
    "Deaths per event of each Problem Type - (Armed Battle/Clash does not include events from the Randa genocide of 1994)")
plt.show()