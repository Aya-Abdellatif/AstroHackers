import sqlite3


con = sqlite3.connect("project.sqlite", check_same_thread=False)
cur = con.cursor()


res = cur.execute('UPDATE Student SET teacher_id = "gead@asd.com"')
con.commit()
