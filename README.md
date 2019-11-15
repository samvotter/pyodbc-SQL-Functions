# pyodbc-SQL-Functions
A collection of SQL Database functions with the help of the pyodbc library.

While the pyodbc library does a bunch of good stuff behind the scenes to connect you with a SQL database, actually performing actions
on that database can be a little clumsy and difficult to automate. This module contains functions which help perform variable-fed
GET statements, conditional WHERE statements, UPDATE CELL and INSERT ROW functions. 

import pyodbc as sql

self.connection = sql.connect(
                driver='{SQL Server}',
                server=server,
                database=db,
                uid=username,
                pwd=password
            )
