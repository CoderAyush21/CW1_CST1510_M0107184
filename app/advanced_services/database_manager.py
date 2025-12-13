import sqlite3
from typing import Any, Iterable


class DatabaseManager:
    '''
    The class Database Manager is for managing database connections and queries
    
    -> Opens and closes the SQlite database connection
    -> Enable execution of CRUD operations
    -> Used instead of importing modules from other files
    -> Thereby, keeping all database management logic in a single class
    '''

    '''
    Initialise database path

    '''
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._connection: sqlite3.Connection | None = None
 

    '''
    Connect to the SQlite database

    '''
    def connect(self) -> None:
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)        
    
    '''
    Close the connection safely

    '''
    def close(self) -> None:
        if self._connection is not None:
            self._connection.close()
            self._connection = None


    '''
    Help execute INSERT, DELETE OR UPDATE operations

    '''
    def execute_query(self, sql: str, params: Iterable[Any] = ()):
    
    
        if self._connection is None:
            self.connect()

        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        self._connection.commit()
        return cur
 

    '''
    Returns only one row of data after execution of a SQL query

    '''
    def fetch_one(self, sql: str, params: Iterable[Any] = ()):
        if self._connection is None:
            self.connect()

        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchone()

    '''
    Returns all matching rows of data after execution of SQL query
    '''
    def fetch_all(self, sql: str, params: Iterable[Any] = ()):
        if self._connection is None:
            self.connect()

        cur = self._connection.cursor()
        cur.execute(sql, tuple(params))
        return cur.fetchall()
