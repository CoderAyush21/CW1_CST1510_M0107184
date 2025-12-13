from datetime import datetime

class Dataset:

    '''
    Class represents a Dataset entity stored in the database
    -> Uses encapsulation to keep data secured using the '__' before attributes
    -> Declare getters to access the attributes

    '''

    def __init__(self, dataset_id, name, rows, columns, uploaded_by=None, upload_date=None):
        '''
        Constructor to initialise a Dataset object
        -> Use of private attributes declaration techniques
        '''
        self.__id = dataset_id
        self.__name = name
        self.__rows = rows
        self.__columns = columns
        self.__uploaded_by = uploaded_by
        self.__upload_date = upload_date

    '''
    Getters to return the attributes

    '''
    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_rows(self) -> int:
        return self.__rows

    def get_columns(self) -> int:
        return self.__columns

    def get_uploaded_by(self) -> str:
        return self.__uploaded_by

    def get_upload_date(self) -> str:
        return self.__upload_date

    '''
    Class method since it creates and returns value without needing to create an instance to use it

    '''
    @classmethod
    def load_by_id(cls, db, dataset_id):

        '''
        Loads a Dataset object from the database using its ID.

        '''
        # Search for required values using sql
        sql = """
            SELECT dataset_id, name, rows, columns, uploaded_by, upload_date
            FROM datasets_metadata
            WHERE dataset_id = ?
        """
        row = db.fetch_one(sql, (dataset_id,))
        if not row:
            return None

        return cls(
            dataset_id=row[0],
            name=row[1],
            rows=row[2],
            columns=row[3],
            uploaded_by=row[4],
            upload_date=row[5]
        )


    '''
    Function to update the name of a dataset

    '''
    def update_name(self, db, name=None, rows=None, columns=None):
        if name is not None:
            self.__name = name
        if rows is not None:
            self.__rows = rows
        if columns is not None:
            self.__columns = columns

        sql = """
            UPDATE datasets_metadata
            SET name = ?, rows = ?, columns = ?
            WHERE dataset_id = ?
        """
        cur = db.execute_query(sql, (
            self.__name,
            self.__rows,
            self.__columns,
            self.__id
        ))
        return cur.rowcount > 0
    

    '''
    Function to insert data in the database for a new dataset

    '''
    def insert_dataset(self, db):
        sql = """
            INSERT INTO datasets_metadata
            (name, rows, columns, uploaded_by, upload_date)
            VALUES (?, ?, ?, ?, ?)
        """
        ts = self.__upload_date if self.__upload_date else datetime.now()
        cur = db.execute_query(sql, (
            self.__name,
            self.__rows,
            self.__columns,
            self.__uploaded_by,
            ts
        ))
        self.__id = cur.lastrowid
        return self.__id
    

    '''
    Delete a dataset function 
    
    '''
    def delete(self, db) -> bool:
        sql = "DELETE FROM datasets_metadata WHERE dataset_id = ?"
        cur = db.execute_query(sql, (self.__id,))
        return cur.rowcount > 0
