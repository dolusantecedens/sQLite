
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except Error as e:
       print(e)

def execute_sql(db_file,code):
    try:
       db_file.cursor().execute(code)
    except Error as e:
       print(e)

def add_book(conn, books):
  sql='''INSERT INTO books( nazwa , genre , release_date ) VALUES ( ? , ? , ? ) '''
  cur=conn.cursor()
  cur.execute(sql,books)
  conn.commit()
  return cur.lastrowid

def add_author(conn, author):
  sql='''INSERT INTO authors(  opis , status , born  ) VALUES ( ? , ? , ? ) '''
  cur=conn.cursor()
  cur.execute(sql, author)
  conn.commit()
  return cur.lastrowid

def select_book(conn,books):
  sql=''' SELECT * FROM books; '''
  conn = create_connection('database.db')
  cur=conn.cursor()
  cur.execute("SELECT * FROM books")
  rows=cur.fetchall()
  return rows



def select_all(conn, table):  
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()
   return rows

def select_where(conn, table, **query):
   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows

def update(conn, table, id, **kwargs):

   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (id, )

   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)

def delete_where(conn, table, **kwargs):
   """
   Delete from table where attributes from
   :param conn:  Connection to the SQLite database
   :param table: table name
   :param kwargs: dict of attributes and values
   :return:
   """
   qs = []
   values = tuple()
   for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)

   sql = f'DELETE FROM {table} WHERE {q}'
   cur = conn.cursor()
   cur.execute(sql, values)
   conn.commit()
   print("Deleted")

def delete_all(conn, table):
   """
   Delete all rows from table
   :param conn: Connection to the SQLite database
   :param table: table name
   :return:
   """
   sql = f'DELETE FROM {table}'
   cur = conn.cursor()
   cur.execute(sql)
   conn.commit()
create_book_library_sql = """
-- books
CREATE TABLE IF NOT EXISTS books (
  id integer PRIMARY KEY,
  nazwa text NOT NULL,
  genre text,
  release_date text
);
"""

create_author_library_sql = """
-- authors
CREATE TABLE IF NOT EXISTS authors (
  id integer PRIMARY KEY,
  opis TEXT,
  status VARCHAR(15) NOT NULL,
  born text NOT NULL,
  FOREIGN KEY (books_id) REFERENCES books (id)
);
"""



db_file = "database.db"

if __name__ == '__main__':
   d=create_connection(db_file)
   if d is not None:
        execute_sql(d,create_book_library_sql)
        execute_sql(d,create_author_library_sql)  
        add_book(d,('main kampf','political','1925'))
        delete_all(d,'books')
        d.close()


