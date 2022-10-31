import sqlite3

conn=sqlite3.connect('db/basedatos.db')
cursor=conn.cursor()







conn.commit()
conn.close()