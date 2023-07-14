import pymysql


def create_tables(cur, conn):
    cur.execute("DROP TABLE IF EXISTS content_articles")
    cur.execute("DROP TABLE IF EXISTS articles")

    cur.execute("""CREATE TABLE articles(
                        id VARCHAR(50) PRIMARY KEY,
                        dt DATETIME NOT NULL,
                        kind_new VARCHAR(40) NOT NULL,
                        reference  VARCHAR(300) NOT NULL,
                        preview VARCHAR(300) NOT NULL,
                        importance VARCHAR(30) NOT NULL
                        )""")

    cur.execute("""CREATE TABLE content_articles(
                        id_article VARCHAR(50),
                        text VARCHAR(4000) NOT NULL,
                        FOREIGN KEY(id_article) REFERENCES articles(id))""")
    conn.commit()


with pymysql.connect(db='first_database', user='root',
                     host='localhost', password='***************') as conn:
    cur = conn.cursor()
    create_tables(cur, conn)
