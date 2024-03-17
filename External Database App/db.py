import pymysql

conn = pymysql.connect(
    host='sql5.freesqldatabase.com',
    database='sql5691881',
    user='sql5691881',
    password='Mg8EUB9Buu',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor();
sql_query = """ CREATE TABLE book (
    id INT PRIMARY KEY AUTO_INCREMENT,
    author text NOT NULL,
    language text NOT NULL,
    title text NOT NULL
)"""
cursor.execute(sql_query)
conn.close()