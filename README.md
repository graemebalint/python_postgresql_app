# python-postgresql-app
A proof of concept program that connects to a postgresql database. The user can create, read, update and delete data in the database through the UI.


Live demo: https://replit.com/@GraemeBalint/python-postgresql-app
Database: https://bit.io/graemebalint/python-postgresql-app


**Instructions:**
1. Open the live demo link and click run. 
2. Open the database link (opens database hosted by bit.io).
3. Verify any changes made to the table via the UI are reflected in the database.


**Project goals:**
1. Learn how to integrate Postgresql with Python
2. Use Python to write directly to a database


**Skills:**
1. Databases
2. Python
3. Postgresql
4. Combining Python and Postgresql together


**Project notes:**
1. All interactions between the Python program and the database are printed on the console. This includes: establishing a connection to the database, committing updates, closing the connection at the end of the session. 
2. The UI and database connection are both classes are made by creating object instances.
3. The UI was built using the Tkinter module in Python. It looks better when rendered locally using a Python compiler like PyCharm. At this point, I have decided to not rebuild the UI for a web app since the focus of this project is working with databases, Python and Postgresql.
