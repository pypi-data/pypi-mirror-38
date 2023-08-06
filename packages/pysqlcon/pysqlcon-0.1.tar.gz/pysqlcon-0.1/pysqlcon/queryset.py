"""
@author: Kudzai Tsapo (kudzai@charteredsys.com)

Description: 
--------------
This file contains the classes for Querying the database
"""
from string import Template
import os

class Row(object):

    def __init__(self, fields, table):
        pass

class Column(object):
    def __init__(self, *args):
        self.sql_statement = ''
        for arg in args:
            self.sql_statement += str(arg) + ' '

    def __str__(self):
        return self.sql_statement

class StoredParam(Column):
    def __init__(self, *args):
        super().__init__(*args)

class BaseObject(object):
    def __init__(self, query_string):
        self.statement = query_string

    def get_statement(self):
        return self.statement

class Table(BaseObject):
    def __init__(self, name, properties=[]):
        if len(properties) == 0:
            raise TypeError("Missing columns")
        
        sql_filepath = os.path.join(os.path.dirname(__file__), 'sql', 'table_creation.sql')
        string_template = Template(open(sql_filepath, 'r').read())
        table_property = ''
        limit = len(properties) - 1
        for count in range(limit):
            table_property += str(properties[count]) + ','
        else:
            table_property += str(properties[limit])

        sql_string = string_template.substitute(tablename=name, properties=table_property)
        super().__init__(sql_string)

class StoredProcedure(BaseObject):
    def __init__(self, name, sql_statement, params=[]):
        sql_filepath = os.path.join(os.path.dirname(__file__), 'sql', 'stored_proc_creation.sql')
        string_template = Template(open(sql_filepath, 'r').read())
        procedure_property = ''
        limit = len(params) - 1
        if len(params) != 0:
            for count in range(limit):
                procedure_property += str(params[count]) + ', '
            else:
                procedure_property += str(params[limit])            


        sql_string = string_template.substitute(procname=name, parameters=procedure_property, body=sql_statement)
        super().__init__(sql_string)

class Query:

    def __init__(self, query, query_type='raw', params=()):
        self.query = query.get_statement() if not isinstance(query, str) else query
        self.query_type = query_type
        self.parameters = params


class Session(object):
    def __init__(self, connection_object):
        #self.query = None
        self.connection = connection_object

    def add(self, query):
        self.connection.execute_query(query.query, query.parameters)

    def add_all(self, queries=[]):
        if len(queries) != 0:
            for query in queries:
                self.add(query)
        else:
            raise EmptyListException("The list of sql queries must not be empty!")

    def query(self, query):
        try:
            if 'sp' in query.query_type.lower():
                self.connection.execute_procedure(query.query, query.parameters)
            else:
                self.connection.execute_query(query.query, query.parameters)

            self.connection.commit()
        except Exception as e:
            raise e


        return True
    
    def query_select(self, query):
        try:
            if 'sp' in query.query_type.lower():
                self.connection.execute_procedure(query.query, query.parameters)
            else:
                self.connection.execute_query(query.query, query.parameters)
        except Exception as e:
            raise e

        rows = self.connection.fetch_rows()
        return rows

