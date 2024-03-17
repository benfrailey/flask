from flask import Flask, request, jsonify
import json
import pymysql

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
    host='sql5.freesqldatabase.com',
    database='sql5691881',
    user='sql5691881',
    password='Mg8EUB9Buu',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
    except pymysql.error as e:
        print(e)
    return conn

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book")
        books = [
            dict(id=row['id'], author=row['author'], language=row['language'], title=row['title'])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books)

    if request.method == 'POST':
        new_author = request.form['author']
        new_lang = request.form['language']
        new_title = request.form['title']

        sql = """INSERT INTO book (author, language, title)
                    VALUES (%s, %s, %s)"""
        cursor.execute(sql, (new_author, new_lang, new_title))
        conn.commit()
        return f"Book with the id: {cursor.lastrowid} created successfully", 201
        
        books_list.append(new_book)
        return jsonify(books_list), 201
    
@app.route('/book/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    book = None
    if request.method == 'GET':
        sql = "SELECT * FROM book WHERE id=%s"
        cursor.execute(sql, (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something wrong", 404

    if request.method == 'PUT':
        sql = """UPDATE book
                SET title=%s,
                    author=%s,
                    language=%s
                WHERE id=%s """
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        updated_book = {
                    'id': id,
                    'author': author,
                    'language': language,
                    'title': title
        }
        cursor.execute(sql, (title, author, language, id))
        conn.commit()
        return jsonify(updated_book)
        
    if request.method == 'DELETE':
        sql = """DELETE from book where id=%s"""
        cursor.execute(sql, (id,))
        conn.commit()
        return "The book with id: {} has been deleted".format(id), 200

@app.route('/tables', methods=['GET', 'POST', 'DELETE'])
def table():
    conn = db_connection()
    cursor = conn.cursor()
    print("hey")
    if request.method == 'GET':
        sql = "SHOW TABLES"
        cursor.execute(sql)
        lst = []
        for tables in cursor.fetchall():
            lst.extend(tables.values())
        return lst
        
    if request.method == 'POST':
        table = request.form['table']
        sql = """ CREATE TABLE {} (
            id INT PRIMARY KEY AUTO_INCREMENT,
            author text NOT NULL,
            language text NOT NULL,
            title text NOT NULL
        )""".format(table)
        cursor.execute(sql)
        conn.commit()
        return "Created table with name: {}".format(table), 200
    
    if request.method == 'DELETE':
        table = request.form['table']
        sql = "DROP TABLE {}".format(table)
        cursor.execute(sql)
        conn.commit()
        return "Dropped table with name: {}".format(table), 200

if __name__ == '__main__':
    app.run(port=8000, debug=True)