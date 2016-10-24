import psycopg2
import psycopg2.extras

def init():
    conn = psycopg2.connect("dbname='monocle' user='monocle_user' host='localhost' password='password'")
    return conn

def q( conn, query):
    kursor = conn.cursor()
    kursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    kursor.execute( query)
    rows = kursor.fetchall()
    return rows

def insertq( conn):
    i =  {
          'happened_on': 'happened_on', 
          "item": 'item', 
          'owner': 'owner', 
          'project': 'project', 
          'shortdesc': 'shortdesc', 
          'status': 'status'
         }
    j = ({"item":"item"},)
    cur = conn.cursor()
    #cur.executemany("""INSERT INTO items VALUES (%(happened_on)s,%(item)s,%(owner)s,%(shortdesc)s,%(project)s,%(status)s )""", i)
    cur.executemany("""INSERT INTO items (item) VALUES ( %(item)s )""", j)
    conn.commit()
    print 'inserted'

def query_example():
    conn = init()
    rows = q( conn, "select * from items")
    for row in rows:
        print "   ", row['id'],row['item']

def insert_example():
    conn = init()
    insertq(conn)

insert_example()
