import psycopg2
import psycopg2.extras

def connect():
    conn = psycopg2.connect(host="127.0.0.1", database="flask-sql-snacks", user="postgres", password="1to1anyherzt");
    return conn

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS snacks (id serial PRIMARY KEY, name text, kind text);")
    conn.commit()
    connect().close()

def close():
    connect().close()

# Implement these methods!

def find_all_snacks():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM snacks")
    snacks = cur.fetchall()
    cur.close()
    conn.close()
    return snacks

def create_snack(name, kind):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO snacks (name, kind) VALUES (%s, %s)", (name, kind,))
    conn.commit()
    cur.close()
    conn.close()

def find_snack(id):
    conn = connect()
    cur = conn.cursor()
    #pg_select = """ SELECT * FROM toys WHERE id = %s """  
    query = f'SELECT * FROM toys WHERE id = {id};'
    #print(query)
    cur.execute("SELECT * FROM snacks WHERE id = (%s)" , (id,))
    #cur.execute(query)
    snacks = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return snacks

def edit_snack(name, kind, id):
    conn = connect()
    cur = conn.cursor()
    snacks = cur.execute("UPDATE snacks SET name = (%s), kind = (%s) WHERE id = (%s)" , (name, kind, id,))
    conn.commit()
    cur.close()
    conn.close()
    return snacks
    
def remove_snack(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM snacks WHERE id = (%s)" , (id,))
    conn.commit()
    cur.close()
    conn.close()
    return id