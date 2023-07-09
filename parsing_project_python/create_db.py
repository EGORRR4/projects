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

def alter_table(cur, conn):
    cur.execute("""ALTER TABLE content_articles 
                        MODIFY COLUMN id_article VARCHAR(50)"""
                )
    cur.execute("""ALTER TABLE articles
                        MODIFY COLUMN id VARCHAR(50)
                        MODIFY COLUMN reference VARCHAR(300)""")
    conn.commit()

with pymysql.connect(db='first_database', user='root', 
                      host='localhost', password='*************') as conn:
    cur = conn.cursor()
    alter_table(cur, conn)
