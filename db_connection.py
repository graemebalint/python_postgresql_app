import psycopg2
from prettytable import from_db_cursor
from config import config

class Database:

   def __init__(self):
      #initiate connection to postgres db
      self.params = config()
      print("Connecting to postgresql database...")
      self.connection = psycopg2.connect(**self.params)
      #create cursor
      self.cursor = self.connection.cursor()

      # check if table exists already
      self.cursor.execute(
         '''
         SELECT EXISTS (
             SELECT FROM
                 pg_tables
             WHERE
                 schemaname = 'public' AND
                 tablename  = 'table1'
             );
         '''
         )
      self.table_exists = self.cursor.fetchone()

      if self.table_exists[0] == False:
         self.cursor.execute(
            '''
               create table table1(
                   id int unique not null primary key
                   , name text
                   , age int
               );
            '''
         )
         self.submit()

      #print database version
      self.cursor.execute('Select version()')
      self.db_version = self.cursor.fetchone()
      print(self.db_version)

   def return_data(self):
      self.cursor.execute("select * from table1 order by id;")
      return(self.cursor.fetchall())

   def primary_key(self):
      #fetch last id
      self.cursor.execute("select id from table1 where id = (select max(id) from table1)")
      self.last_id = self.cursor.fetchone()

      if self.last_id == None:
         self.next_id = 1
      else:
         self.next_id = self.last_id[0] + 1
      return self.next_id

   def submit(self):
      self.connection.commit()
      print("Update commited to db")

   def terminate(self):
      self.cursor.close()
      self.connection.close()
      print("Connection to database terminated.")