'''
Author: Sam Van Otterloo

This module contains generic re-usable SQL database functions
'''

from typing import List
from Debugging import print_n_warn
from pyodbc import connect


# The main function for interacting with the database
#   connection is the the link through pyodbc to the sql database
#   table is where you are looking
#   target is the column you want
#   condition is the statement (or series of statements) being tested
#       condition is generated using the where() function
def get(
        connection: connect,
        table: str = None,
        targets: str = None,
        condition: str = None
) -> List:
    # create temporary cursor, performs the actual database query
    cursor = connection.cursor()
    # take the whole table
    if targets is None:
        strings = [table]
        try:
            results = cursor.execute(
                r"SELECT * FROM {}".format(*strings)
            )
            return results.fetchall()
        except:
            print_n_warn("ERROR! Not able to get data from {}.".format(table))
    # take a column from the table
    elif condition is None:
        strings = [targets, table]
        try:
            results = cursor.execute(
                r"SELECT {} FROM {}".format(*strings)
            )
            results.fetchall()
        except:
            print_n_warn("ERROR! Not able to get {} from {}.".format(targets, table))
    # take a Tuple of specific values from the table
    elif table and targets and condition:
        strings = [targets, table, condition]
        try:
            results = cursor.execute(
                r"SELECT {} FROM {} {}".format(*strings)
            )
            return results.fetchall()
        except:
            print_n_warn("ERROR! Not able to get {} from {} where {}".format(targets, table, condition))
    else:
        # ERROR! should be unreachable
        return [None]


# Helper function that creates conditional statements for self.get.
# You should be able to read them left-to-right like if statements
    # conditions['variable_name'] = [operator, 'val']
    # EXAMPLE: 'CustomerName' = ['!=', 'Dell']
    # Means: find me something WHERE 'CustomerName != 'Dell'
def where(
        **conditions
) -> str:
    keys = list(conditions.keys())
    # for just one condition
    buffer: str = "WHERE {} {} '{}'".format(
        keys[0],
        conditions[keys[0]][0],
        conditions[keys[0]][1]
    )
    if len(keys) > 1:
        # for multiple conditions
        for item in keys[1:]:
            buffer += " AND {} {} '{}'".format(
                item,
                conditions[item][0],
                conditions[item][1]
            )
    return buffer


# update a specific cell of a specific table
#   connection is the the link through pyodbc to the sql database
#   column is the column of the value you want to change
#   set_to is the new data being put into the cell
def update_cell(
        connection: connect,
        table: str,
        column: str,
        set_to,
        condition: str
) -> None:
    # create temporary cursor, performs the actual database query
    cursor = connection.cursor()
    cursor.execute(r"UPDATE {} SET {} = '{}' {}".format(
        table, column, set_to, condition
    ))
    connection.commit()


# put rows into a given table
#   connection is the the link through pyodbc to the sql database
#   you must know what columns are in the table that you would like to insert into
#       vals are the columns ordered list of inputs to insert
#   all string input values are converted to uppercase and stripped of whitespace to avoid case-confusion
def insert_rows(
        connection: connect,
        table: str,
        columns: List[str],
        *vals: List
) -> None:
    buffer = f"INSERT INTO {table} ("
    for col in columns:
        buffer += f"{col}, "
    buffer = buffer[:-2]
    buffer += ") VALUES "
    for val_set in vals:
        val_string = "("
        for val in val_set:
            if isinstance(val, str):
                val = f"'{val.lower().strip()}'"
            val_string += f"{val}, "
        val_string = val_string[:-2]
        val_string += "), "
        buffer += val_string
    buffer = buffer[:-2]
    # create temporary cursor, performs the actual database actions
    cursor = connection.cursor()
    cursor.execute(buffer)
    connection.commit()
