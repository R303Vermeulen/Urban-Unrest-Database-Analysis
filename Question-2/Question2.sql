# note that this file is a recap of the sql queries used in Question2.py


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
    maxc AS ( SELECT c.Country
              FROM conts c, maxdeathc m
              WHERE c.deathTot = m.mdc ),
    sumds AS ( SELECT md.Ptype, SUM(maxd) as deathTot
               FROM maxds md, Countries co, Cities ci, maxc mc, ProblemTypes p
               WHERE co.ISO3 = ci.Country and
                     ci.CityId = md.City and
                     (co.Country != mc.Country or
                      (md.Ptype = p.Ptype and
                       p.ProblemType != 'Armed Battle/Clash'))
               GROUP BY Ptype )
SELECT p.Ptype, p.ProblemType, s.deathTot
FROM ProblemTypes p, sumds s
WHERE p.Ptype = s.Ptype
ORDER BY s.deathTot DESC;



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
    maxc AS ( SELECT c.Country
              FROM conts c, maxdeathc m
              WHERE c.deathTot = m.mdc ),
    sumds AS ( SELECT md.Ptype, SUM(maxd) as deathTot
               FROM maxds md, Countries co, Cities ci, maxc mc, ProblemTypes p
               WHERE co.ISO3 = ci.Country and
                     ci.CityId = md.City and
                     (co.Country != mc.Country or
                      (md.Ptype = p.Ptype and
                       p.ProblemType != 'Armed Battle/Clash'))
               GROUP BY Ptype )
    psums AS ( SELECT p.Ptype, p.ProblemType, s.deathTot \n"
               FROM ProblemTypes p, sumds s
               WHERE p.Ptype = s.Ptype
               ORDER BY s.deathTot DESC ),
    maxpsum AS ( SELECT MAX(deathTot) as mps
                 FROM psums ),
    maxpt AS ( SELECT p.ProblemType, p.deathTot
               FROM psums p, maxpsum m
               WHERE p.deathTot = m.mps )
SELECT DISTINCT maxc.Country, maxpt.ProblemType, maxpt.deathTot
FROM maxc, maxpt ;



