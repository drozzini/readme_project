# Utilitários para MariaDB
import os
import mariadb

def get_connection():
    return mariadb.connect(
        user=os.getenv("MARIADB_USER", "root"),
        password=os.getenv("MARIADB_PASSWORD", ""),
        host=os.getenv("MARIADB_HOST", "localhost"),
        port=int(os.getenv("MARIADB_PORT", 3306)),
        database=os.getenv("MARIADB_DATABASE", "readme_db")
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    # Tabela principal com times admin/maintainer
    cur.execute("""
    CREATE TABLE IF NOT EXISTS readme_results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        repo VARCHAR(255),
        status VARCHAR(32),
        detalhe TEXT,
        teams_admin TEXT,
        teams_maintainer TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """)
    # Tabela relacional para granularidade
    cur.execute("""
    CREATE TABLE IF NOT EXISTS repo_teams (
        id INT AUTO_INCREMENT PRIMARY KEY,
        repo VARCHAR(255),
        team VARCHAR(255),
        role VARCHAR(32),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """)
    conn.commit()
    cur.close()
    conn.close()


def save_result(repo, status, detalhe, teams_admin=None, teams_maintainer=None, teams_granular=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO readme_results (repo, status, detalhe, teams_admin, teams_maintainer) VALUES (?, ?, ?, ?, ?)",
        (repo, status, detalhe, teams_admin or '', teams_maintainer or '')
    )
    # Grava granularidade na tabela repo_teams
    if teams_granular:
        for t in teams_granular:
            cur.execute(
                "INSERT INTO repo_teams (repo, team, role) VALUES (?, ?, ?)",
                (repo, t['team'], t['role'])
            )
    conn.commit()
    cur.close()
    conn.close()
