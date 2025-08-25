# Queries SQL para análise de aderência dos READMEs
# Use conforme o banco (MariaDB ou PostgreSQL)

-- 1. Evolução de aderência ao longo do tempo (contagem diária)
-- MariaDB/PostgreSQL:
SELECT DATE(created_at) AS dia, status, COUNT(*) AS total
FROM readme_results
GROUP BY dia, status
ORDER BY dia DESC, status;

-- 2. Aderência por time admin
-- MariaDB/PostgreSQL:
SELECT teams_admin, status, COUNT(*) AS total
FROM readme_results
GROUP BY teams_admin, status
ORDER BY teams_admin, status;

-- 3. Aderência por time maintainer
-- MariaDB/PostgreSQL:
SELECT teams_maintainer, status, COUNT(*) AS total
FROM readme_results
GROUP BY teams_maintainer, status
ORDER BY teams_maintainer, status;

-- 4. Aderência por time granular (tabela repo_teams)
-- MariaDB/PostgreSQL:
SELECT t.team, t.role, r.status, COUNT(*) AS total
FROM repo_teams t
JOIN readme_results r ON t.repo = r.repo
GROUP BY t.team, t.role, r.status
ORDER BY t.team, t.role, r.status;

-- 5. Evolução geral de aderência (percentual)
-- MariaDB/PostgreSQL:
SELECT dia, 
       SUM(CASE WHEN status = 'Aderente' THEN 1 ELSE 0 END) AS aderentes,
       SUM(CASE WHEN status = 'Não aderente' THEN 1 ELSE 0 END) AS nao_aderentes,
       COUNT(*) AS total,
       ROUND(100.0 * SUM(CASE WHEN status = 'Aderente' THEN 1 ELSE 0 END) / COUNT(*), 2) AS perc_aderencia
FROM (
  SELECT DATE(created_at) AS dia, status
  FROM readme_results
) sub
GROUP BY dia
ORDER BY dia DESC;
