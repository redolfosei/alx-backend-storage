-- SQL script which ranks country origins of bands, and
-- Ordered by the number of (non-unique) fans
-- Script can be executed on any database
SELECT origin, SUM(fans) as nb_fans
FROM metal_bands
GROUP BY origin
ORDER BY nb_fans DESC;
