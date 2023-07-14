import pymysql


def update_db(cur, conn):
    cur.execute("""DELETE FROM content_articles
                    WHERE DATE(dt) < DATE_SUB(NOW(),INTERVAL 30 DAY); """)
    cur.execute("""DELETE FROM articles
                        WHERE DATE(dt) < DATE_SUB(NOW(),INTERVAL 30 DAY); """)
    conn.commit()


with pymysql.connect(db='first_database', user='root',
                     host='localhost', password='1212313111123') as conn:
    cur = conn.cursor()
    create_tables(cur, conn)