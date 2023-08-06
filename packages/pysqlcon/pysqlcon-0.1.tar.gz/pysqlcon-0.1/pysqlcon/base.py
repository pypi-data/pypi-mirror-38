"""
@author: Kudzai Tsapo (kudzai@charteredsys.com)

Description: 
--------------
This file contains the model class for abstracting the execution of stored procedures and sql queries
as well as fetching rows from a SQL Server database.
"""
import pyodbc 

class PySQLCon(object):
    """
        This connects to any SQL Server database and executes stored procedures saved 
        in that database as well as raw SQL queries.

        Parameters
        ----------
        server : str
            The hostname/IP address of the server which hosts the database

        database : str
            The database you wish to connect to (Should exist)
        username : str
            The username for the database server
        password: str
            The password for the username
    """
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER='+self.server+';DATABASE='+self.database+';UID='+self.username+';PWD='+ self.password)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        """ Closes the connection to the database """
        self.cursor.close()

    def execute_procedure(self, procname, params=()):
        """
          This executes stored procedures stored in the database 
          Parameters:
          -----------
          procname: str
                    The name of the stored procedure you wish to execute
          params (optional): tuple
                The parameters you wish to pass to the stored procedure
        """
        sql = "exec [" + self.database + "].[dbo].[" + procname + "]"
        if len(params) != 0:
            for count in range(1, len(params)):
                sql += "?,"
            else:
                sql += "?" 
            
        if len(params) != 0:
            self.cursor.execute(sql, (params))
        else:
            self.cursor.execute(sql)

    def commit(self):
        self.cursor.commit()

    def execute_query(self, query, params=()):
        """
          This executes raw SQL queries on the database 
          Parameters:
          -----------
          query: str
                The query you wish to execute

          params (optional): tuple
                Parameters to be passed to the query
        """
        if len(params) != 0:
            self.cursor.execute(query, (params))
        else:
            self.cursor.execute(query)

    def execute_file(self, filepath, params=()):
        """
          This executes queries stored in an .sql file 
          Parameters:
          -----------
          filepath: str
                The file you wish to execute, as a path eg. C:\\Users\\someone\\Documents\\file.sql

          params (optional): str
                The parameters to pass to the SQL script  
        """
        if not filepath.endswith('.sql'):
            raise InvalidFileException("The file does not have a .sql extension!")
        else:
            sql_statements = open(filepath, 'r').read()
            self.execute_query(sql_statements, params)

    def fetch_rows(self):
        """
        Fetches rows from executed stored procedure or sql query
        
        Returns
        --------
        list 
            a list of rows returned from the stored procedure or sql query
        """
        rows = self.cursor.fetchall()
        return rows

    def fetch_row(self):
        """
        Fetches a single from executed stored procedure or sql query
        
        Returns
        --------
        tuple 
            a tuple of data returned from the stored procedure or sql query
        """
        row = self.cursor.fetchone()
        return row
