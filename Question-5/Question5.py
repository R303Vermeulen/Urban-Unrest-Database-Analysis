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
                       "END as maxd, Ptype, City \n"
                       "FROM Events \n"
                       "WHERE deathFlag = 1 ), \n"
                       "contstot AS ( SELECT co.Country, SUM(m.maxd) as deathTot \n"
                       "FROM Countries co, Cities ci, maxds m \n"
                       "WHERE co.ISO3 = ci.Country and \n"
                       "ci.CityId = m.City \n"
                       "GROUP BY co.ISO3, co.Country ), \n"
                       "contscapstot AS ( SELECT co.Country, SUM(m.maxd) as deathTot \n"
                       "FROM Countries co, Cities ci, maxds m \n"
                       "WHERE co.ISO3 = ci.Country and \n"
                       "ci.CityId = m.City and \n"
                       "ci.isCapital = 1 \n"
                       "GROUP BY co.ISO3, co.Country ), \n"
                       "contratios AS ( SELECT ct.Country, cct.deathTot/ct.deathTot * 100 AS ratio \n"
                       "FROM contstot ct LEFT JOIN contscapstot cct ON ct.Country = cct.Country \n"
                       "ORDER BY ratio DESC ) \n "
                       "SELECT c.Country, CASE \n"
                       "WHEN c.ratio > 50 THEN 1 \n"
                       "WHEN c.ratio <= 50 THEN 0 \n"
                       "WHEN c.ratio is null THEN 0 \n"
                       "END as 'MajorityInCapital?' \n"
                       "FROM contratios c;")

        records = cursor.fetchall()
        pyth1 = records

        # print("---------------------------------------")
        # for r in records:
        #    print(r)
        # print("---------------------------------------")


except Error as e:
    print('Connection error: ', e)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print('Done')

######################### to turn into map

contList = ['Andorra', 'United Arab Emirates', 'Afghanistan', 'Albania', 'Armenia', 'Angola', 'Antarctica', 'Argentina',
            'Austria', 'Australia', 'Azerbaijan',
            'Bosnia and Herzegovina', 'Bangladesh', 'Belgium', 'Burkina Faso', 'Bulgaria', 'Bahrain', 'Burundi',
            'Benin', 'Brunei Darussalam', 'Bolivia',
            'Brazil', 'Bhutan', 'Botswana', 'Belarus', 'Belize', 'Canada', 'Congo, DRC', 'Central African Republic',
            'Congo', 'Switzerland',
            "Cote d'Ivoire", 'Chile', 'Cameroon', 'China', 'Colombia', 'Costa Rica', 'Cuba', 'Cape Verde', 'Cyprus',
            'Czech Republic', 'Germany', 'Djibouti', 'Denmark',
            'Dominican Republic', 'Algeria', 'Ecuador', 'Estonia', 'Egypt', 'Western Sahara', 'Eritrea', 'Spain',
            'Ethiopia', 'Finland', 'France', 'Gabon', 'United Kingdom', 'Georgia',
            'French Guiana', 'Ghana', 'Greenland', 'Gambia', 'Guinea', 'Equatorial Guinea', 'Greece', 'Guatemala',
            'Guam', 'Guinea-Bissau', 'Guyana', 'Hong Kong', 'Honduras', 'Croatia',
            'Haiti', 'Hungary', 'Indonesia', 'Ireland', 'Israel', 'India', 'Iraq', 'Iran', 'Iceland', 'Italy',
            'Jamaica', 'Jordan', 'Japan', 'Kenya', 'Kyrgyzstan',
            'Cambodia', 'Korea, Democratic People’s Republic of', 'South Korea', 'Kuwait', 'Kazakhstan', 'Laos',
            'Lebanon', 'Liechtenstein',
            'Sri Lanka', 'Liberia', 'Lesotho', 'Lithuania', 'Luxembourg', 'Latvia', 'Libya', 'Morocco', 'Monaco',
            'Moldova, Republic of', 'Montenegro', 'Madagascar',
            'Macedonia, the former Yugoslav Republic of', 'Mali', 'Myanmar', 'Mongolia', 'Macao', 'Mauritania', 'Malta',
            'Mauritius', 'Maldives', 'Malawi', 'Mexico', 'Malaysia',
            'Mozambique', 'Namibia', 'Niger', 'Nigeria', 'Nicaragua', 'Netherlands', 'Norway', 'Nepal', 'New Zealand',
            'Oman', 'Panama', 'Peru', 'Papua New Guinea', 'Philippines',
            'Pakistan', 'Poland', 'Puerto Rico', 'Palestine, State of', 'Portugal', 'Paraguay', 'Reunion', 'Romania',
            'Serbia', 'Russian Federation', 'Rwanda', 'Saudi Arabia',
            'Seychelles', 'Sudan', 'Sweden', 'Singapore', 'Saint Helena, Ascension and Tristan da Cunha', 'Slovenia',
            'Slovakia', 'Sierra Leone', 'San Marino', 'Senegal', 'Somalia',
            'Suriname', 'Sao Tome and Principe', 'El Salvador', 'Syria', 'Swaziland', 'Chad', 'Togo', 'Thailand',
            'Tajikistan', 'Timor-Leste', 'Turkmenistan',
            'Tunisia', 'Turkey', 'Taiwan', 'Tanzania', 'Ukraine', 'Uganda', 'United States', 'Uruguay', 'Uzbekistan',
            'Holy See (Vatican City State)', 'Venezuela', 'Vietnam', 'Yemen', 'Mayotte', 'South Africa', 'Zambia',
            'Zimbabwe']

abbrevList = ['ad', 'ae', 'af', 'al', 'am', 'ao', 'aq', 'ar', 'at', 'au', 'az', 'ba', 'bd', 'be', 'bf', 'bg', 'bh',
              'bi', 'bj', 'bn', 'bo', 'br', 'bt', 'bw', 'by', 'bz', 'ca', 'cd', 'cf', 'cg',
              'ch', 'ci', 'cl', 'cm', 'cn', 'co', 'cr', 'cu', 'cv', 'cy', 'cz', 'de', 'dj', 'dk', 'do', 'dz', 'ec',
              'ee', 'eg', 'eh', 'er', 'es', 'et', 'fi', 'fr', 'ga', 'gb', 'ge', 'gf', 'gh',
              'gl', 'gm', 'gn', 'gq', 'gr', 'gt', 'gu', 'gw', 'gy', 'hk', 'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il',
              'in', 'iq', 'ir', 'is', 'it', 'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'kp', 'kr',
              'kw', 'kz', 'la', 'lb', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'me', 'mg',
              'mk', 'ml', 'mm', 'mn', 'mo', 'mr', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz',
              'na', 'ne', 'ng', 'ni', 'nl', 'no', 'np', 'nz', 'om', 'pa', 'pe', 'pg', 'ph', 'pk', 'pl', 'pr', 'ps',
              'pt', 'py', 're', 'ro', 'rs', 'ru', 'rw', 'sa', 'sc', 'sd', 'se', 'sg', 'sh',
              'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'sv', 'sy', 'sz', 'td', 'tg', 'th', 'tj', 'tl', 'tm',
              'tn', 'tr', 'tw', 'tz', 'ua', 'ug', 'us', 'uy', 'uz', 'va', 've', 'vn', 'ye',
              'yt', 'za', 'zm', 'zw']

cones = []
ceros = []

for i in pyth1:
    if i[1] == 1:
        cones.append(i[0])
    else:
        ceros.append(i[0])

a1list = []
for i in cones:
    if i in contList:
        dex = contList.index(i)
        a1list.append(abbrevList[dex])

a0list = []
for i in ceros:
    if i in contList:
        dex = contList.index(i)
        a0list.append(abbrevList[dex])

otralist = []
for i in abbrevList:
    if i not in cones and i not in ceros:
        otralist.append(i)

custom_style = Style(colors=('#FF0000', '#0000FF', '#00FF00'))

# create a world map,
# Style class is used for using
# the custom colours in the map,
worldmap = pygal.maps.world.World(style
                                  =custom_style)

# set the title of the map
worldmap.title = 'For Each Country, Have a Majority of The Deaths From Urban Unrest Events Been Within The Capital City?'

# hex code of colours are used
# for every .add() called
worldmap.add('Yes', a1list)
worldmap.add('No', a0list)
worldmap.add('No Deaths in DB', otralist)

# save into the file
worldmap.render_to_file('Capitals.svg')
