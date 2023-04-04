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

        cursor.execute("WITH \n"
                       "maxds AS ( SELECT CASE \n"
                       "WHEN maxDeaths = -1 THEN minDeaths \n"
                       "WHEN maxDeaths > -1 THEN maxDeaths \n"
                       "END as maxd, Ptype \n"
                       "FROM Events \n"
                       "WHERE deathFlag = 1 ), \n"
                       "sumds AS ( SELECT Ptype, SUM(maxd) as deathTot \n"
                       "FROM maxds \n"
                       "GROUP BY Ptype ) \n"
                       "SELECT p.Ptype, p.ProblemType, s.deathTot \n"
                       "FROM ProblemTypes p, sumds s \n"
                       "WHERE p.Ptype = s.Ptype \n"
                       "ORDER BY s.deathTot DESC;")

        records = cursor.fetchall()
        pyth1 = records

        cursor.execute(
            "WITH \n"
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
            "sumds AS ( SELECT Ptype, SUM(maxd) as deathTot \n"
            "FROM maxds md, Countries co, Cities ci, maxc mc \n"
            "WHERE co.ISO3 = ci.Country and \n"
            "ci.CityId = md.City and \n"
            "co.Country = mc.Country \n"
            "GROUP BY Ptype ) \n"
            "SELECT p.Ptype, p.ProblemType, s.deathTot \n"
            "FROM ProblemTypes p, sumds s \n"
            "WHERE p.Ptype = s.Ptype \n"
            "ORDER BY s.deathTot DESC;")

        records = cursor.fetchall()
        pyth2 = records

        cursor.execute(
            "WITH \n"
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
            "WHERE c.deathTot = m.mdc ) \n"
            "SELECT * \n"
            "FROM maxc;")

        records = cursor.fetchall()
        pyth3 = records

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

###### now analyzing return from query for first pie graph
l = len(pyth1)
data = []
for i in range(l):
    data.append(int(pyth1[i][2]))

labs = []
for i in range(l):
    labs.append(pyth1[i][1])

# Creating plot
fig, ax = plt.subplots(figsize=(10, 7))
wedges, autotexts = ax.pie(data, labels=labs,
                           startangle=180)

# Adding legend
ax.legend(wedges, labs,
          title="Problem Type",
          loc="upper left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.setp(autotexts, size=8)
ax.set_title(
    "Distribution of Total Deaths Per Problem Type Out of All Total Deaths, From All Events That Occured Globally")

# show plot
plt.show()

############ finding country with highest death total
print(pyth3[0][0])

###### now analyzing return from query for second pie graph
l = len(pyth2)
data = []
for i in range(l):
    data.append(int(pyth2[i][2]))

labs = []
for i in range(l):
    labs.append(pyth2[i][1])

# Creating plot
fig, ax = plt.subplots(figsize=(10, 7))
wedges, autotexts = ax.pie(data, labels=labs,
                           startangle=180)

# Adding legend
ax.legend(wedges, labs,
          title="Problem Type",
          loc="upper left",
          bbox_to_anchor=(1, 0, 0.5, 1))

tittext = "Distribution of Total Deaths Per Problem Type Out of All Total Deaths,"
tittext += " From All Events That Occured in The Country With the Most Total Deaths Globally "
tittext += '(' + pyth3[0][0] + ')'
plt.setp(autotexts, size=8)
ax.set_title(tittext)

# show plot
plt.show()

print(pyth3[0][0])
