import sqlite3

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.

for row in cur.execute('SELECT * FROM Fridges ORDER BY price'):
        print(row)



