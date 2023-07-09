import pymysql
import re

def create_tables(cur, conn):
    
    cur.execute("""CREATE TABLE articles(
                        id VARCHAR(20) PRIMARY KEY,
                        dt DATETIME NOT NULL,
                        reference  VARCHAR(100) NOT NULL,
                        preview VARCHAR(300),
                        importance VARCHAR(30)
                        )""")
    
    cur.execute("""CREATE TABLE content_articles(
                        id_article VARCHAR(20),
                        text VARCHAR(16000),
                        FOREIGN KEY(id_article) REFERENCES articles(id))""")
    conn.commit()

with pymysql.connect(db='first_database', user='root', 
                      host='localhost', password='*************') as conn:
    cur = conn.cursor()
    create_tables(cur, conn)
