# note that this file is a recap of the sql queries used in Question3.py


(WITH
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
     maxc AS ( SELECT c.Country
               FROM conts c, maxdeathc m
               WHERE c.deathTot = m.mdc ),
     dperes AS ( SELECT md.Ptype, SUM(maxd)/COUNT(*) as dpere
                 FROM maxds md, Countries co, Cities ci, maxc mc, ProblemTypes p
                 WHERE co.ISO3 = ci.Country and
                       ci.CityId = md.City and
                       (co.Country != mc.Country or
                        (md.Ptype = p.Ptype and
                         p.ProblemType != 'Armed Battle/Clash'))
                 GROUP BY md.Ptype )
 SELECT p.ProblemType, d.dpere
 FROM ProblemTypes p, dperes d
 WHERE p.Ptype = d.Ptype
 ORDER BY d.dpere DESC)
UNION
(WITH
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
     maxc AS ( SELECT c.Country
               FROM conts c, maxdeathc m
               WHERE c.deathTot = m.mdc ),
     dperes AS ( SELECT md.Ptype, SUM(md.maxd)/COUNT(*) as dpere
                 FROM maxds md, Countries co, Cities ci, maxc mc, ProblemTypes p
                 WHERE co.ISO3 = ci.Country and
                       ci.CityId = md.City and
                       co.Country = mc.Country and
                       md.Ptype = p.Ptype and
                       md.maxd > 10000 and
                       p.ProblemType = 'Armed Battle/Clash'
                 GROUP BY md.Ptype )
 SELECT p.ProblemType, d.dpere
 FROM ProblemTypes p, dperes d
 WHERE p.Ptype = d.Ptype)
ORDER BY dpere DESC;