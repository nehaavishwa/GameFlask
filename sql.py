import sqlite3

with sqlite3.connect("sample.db") as connection:
	c = connection.cursor()
	c.execute("""Create Table posts(title TEXT, description TEXT)""")
	c.execute('Insert Into posts values("Good", "Well")')
	c.execute('Insert Into posts values("Excellent", "OK")')