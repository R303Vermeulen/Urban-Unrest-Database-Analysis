# note that this file is a recap of the sql queries used in Question5.py


WITH
    maxds AS ( SELECT CASE
                 WHEN maxDeaths = -1 THEN minDeaths
                 WHEN maxDeaths > -1 THEN maxDeaths
                      END as maxd, Ptype, City
               FROM Events
               WHERE deathFlag = 1 ),
    contstot AS ( SELECT co.Country, SUM(m.maxd) as deathTot
                  FROM Countries co, Cities ci, maxds m
                  WHERE co.ISO3 = ci.Country and
                        ci.CityId = m.City
                  GROUP BY co.ISO3, co.Country ),
    contscapstot AS ( SELECT co.Country, SUM(m.maxd) as deathTot
                      FROM Countries co, Cities ci, maxds m
                      WHERE co.ISO3 = ci.Country and
                            ci.CityId = m.City and
                            ci.isCapital = 1
                      GROUP BY co.ISO3, co.Country ),
    contratios AS ( SELECT ct.Country, cct.deathTot/ct.deathTot * 100 AS ratio
                    FROM contstot ct LEFT JOIN contscapstot cct ON ct.Country = cct.Country
                    ORDER BY ratio DESC )
SELECT c.Country, CASE
           WHEN c.ratio > 50 THEN 1
           WHEN c.ratio <= 50 THEN 0
           WHEN c.ratio is null THEN 0
                  END as 'MajorityInCapital?'
FROM contratios c;