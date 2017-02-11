import sqlite3
conn = sqlite3.connect('philadelphia.db')

cur = conn.cursor()

# create nodes table
cur.execute('''CREATE TABLE Nodes
                (id INTEGER PRIMARY KEY, lat REAL, long REAL, user VARCHAR,
                uid INTEGER, version INTEGER, changeset INTEGER, timestamp
                VARCHAR)''')

conn.commit()

cur.execute('''CREATE TABLE nodesTags
                (id INTEGER, key VARCHAR, value VARCHAR, type VARCHAR,
                FOREIGN KEY (id) REFERENCES Nodes(id))''')

conn.commit()

cur.execute('''CREATE TABLE Ways
                (id INTEGER PRIMARY KEY, user VARCHAR, uid INTEGER, version INTEGER,
                changeset INTEGER, timestamp VARCHAR)''')

conn.commit()

cur.execute('''CREATE TABLE waysNodes
                (id INTEGER, node_id INTEGER, position INTEGER,
                FOREIGN KEY (id) REFERENCES Nodes(id))''')

conn.commit()

cur.execute('''CREATE TABLE waysTags
            (id INTEGER, key VARCHAR, value VARCHAR, type VARCHAR,
            FOREIGN KEY (id) REFERENCES Ways(id))''')

conn.commit()

conn.close()
