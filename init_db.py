import sqlite3

con = sqlite3.connect("news.db")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS categorey(id, categorey_name)")
cur.execute("""
INSERT INTO categorey (id, categorey_name)
VALUES ("1", "News"),
("2", "Sports"),
("3", "Finance")
""")
con.commit()

