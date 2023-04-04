# note that this file is a recap of the sql queries used in Question4.py

WITH
    maxds AS ( SELECT CASE
                 WHEN maxDeaths = -1 THEN minDeaths
                 WHEN maxDeaths > -1 THEN maxDeaths
                      END as maxd, Ptype, City
               FROM Events
               WHERE deathFlag = 1 ),
    conts AS ( SELECT co.Country, SUM(m.maxd) as deathTot
               FROM Countries co, Cities ci, maxds m
               WHERE co.ISO3 = ci.Country and
                     ci.CityId = m.City
               GROUP BY co.ISO3, co.Country ),
    maxdeathc AS ( SELECT MAX(deathTot) as mdc
                   FROM conts ),
    maxc AS ( SELECT c.Country, c.deathTot
              FROM conts c, maxdeathc m
              WHERE c.deathTot = m.mdc ),
    tot AS ( SELECT 'Everywhere Else' as Country, SUM(deathTot) as deathTot
             FROM conts )
(SELECT * FROM tot)
UNION
(Select * FROM maxc);