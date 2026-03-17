import sqlite3
import anvil.server
from anvil.files import data_files

DB_PATH = data_files["WHA-Meisterliga.db"]

def get_conn():
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  return conn

@anvil.server.callable
def get_seasons():
  conn = get_conn()
  cur = conn.cursor()
  cur.execute("""
        SELECT season_id, name
        FROM Season
        ORDER BY season_id
    """)
  rows = [dict(r) for r in cur.fetchall()]
  conn.close()
  return rows

@anvil.server.callable
def get_table_for_season(season_id):
  conn = get_conn()
  cur = conn.cursor()
  cur.execute("""
        SELECT
            t.name AS mannschaft,
            sr.spiele,
            sr.siege,
            sr.unentschieden,
            sr.niederlagen,
            sr.tore,
            sr.gegentore,
            (sr.tore - sr.gegentore) AS differenz,
            sr.punkte
        FROM Season_Result sr
        JOIN Team t ON sr.team_id = t.team_id
        WHERE sr.season_id = ?
        ORDER BY sr.punkte DESC, differenz DESC, sr.tore DESC
    """, (season_id,))

  rows = [dict(r) for r in cur.fetchall()]
  conn.close()

  for i, row in enumerate(rows, start=1):
    row["rang"] = i

  return rows

@anvil.server.callable
def get_points_chart_data(season_id):
  conn = get_conn()
  cur = conn.cursor()
  cur.execute("""
        SELECT
            t.name AS team,
            sr.punkte
        FROM Season_Result sr
        JOIN Team t ON sr.team_id = t.team_id
        WHERE sr.season_id = ?
        ORDER BY sr.punkte DESC
    """, (season_id,))

  rows = [dict(r) for r in cur.fetchall()]
  conn.close()
  return rows

@anvil.server.callable
def get_goals_chart_data(season_id):
  conn = get_conn()
  cur = conn.cursor()
  cur.execute("""
        SELECT
            t.name AS team,
            sr.tore,
            sr.gegentore
        FROM Season_Result sr
        JOIN Team t ON sr.team_id = t.team_id
        WHERE sr.season_id = ?
        ORDER BY sr.tore DESC
    """, (season_id,))

  rows = [dict(r) for r in cur.fetchall()]
  conn.close()
  return rows

@anvil.server.callable
def get_matches_for_season(season_id):
  conn = get_conn()
  cur = conn.cursor()
  cur.execute("""
        SELECT
            m.match_id,
            m.datum_zeit,
            m.status,
            ht.name AS heimteam,
            at.name AS auswaertsteam,
            mr.heim_tore,
            mr.auswaerts_tore
        FROM Match m
        JOIN Team ht ON m.heim_team_id = ht.team_id
        JOIN Team at ON m.auswaerts_team_id = at.team_id
        LEFT JOIN Match_Result mr ON m.match_id = mr.match_id
        WHERE m.season_id = ?
        ORDER BY m.datum_zeit
    """, (season_id,))

  rows = [dict(r) for r in cur.fetchall()]
  conn.close()
  return rows