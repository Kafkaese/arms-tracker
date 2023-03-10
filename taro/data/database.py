import sqlite3
from sqlite3 import Error
import os

def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(database=os.getenv["DB_PATH"])
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            
def create_write_dict_db(table_name: str, data: dict, verbose = False):
    """
    Writes the contents of a dictionary into a table in the database
    ! DESTRUCTIVE: overwrites pre-existing table of same name
    """
    sqliteConnection = None
    try:
    
        # Connect to databse
        sqliteConnection = sqlite3.connect(database=os.getenv("DB_PATH"))
        cursor = sqliteConnection.cursor()

        # Drop old table of same name
        cursor.execute(f"drop table if exists {table_name}")
    
        # create field names for table from dictionary keys
        data_types = {'int': 'INTEGER', 'float': 'REAL', 'str': 'TEXT'}
        
        field_names = [f'{key} {data_types[type(value).__name__]}' for key, value in data.items()]
        field_names = ', '.join(field_names)
        
        # Create country table 
        cursor.execute(f'create table {table_name} ({field_names});') 
        
        # Insert data into table
        keys = ', '.join(data.keys())
        values = tuple([str(value) for value in data.values()])
        print(len(values))
        print(f"insert into {table_name} ({keys}) VALUES ({('?, '*len(values)).strip(', ')});")
        cursor.executemany(f"insert into {table_name} ({keys}) VALUES ({('?, '*len(values)).strip(', ')});", [values])
    
        # Show student table
        if verbose:
            cursor.execute(f'select * from {table_name};')
    
            # View result
            result = cursor.fetchall()
            print(result)
    
        # Commit work and close connection
        sqliteConnection.commit()
        cursor.close()
    
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print('SQLite Connection closed')

def insert_country(db_path, country):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """
    try:
        # Connect to SQLite
        conn = sqlite3.connect(database=db_path)
        
        
        sql = ''' INSERT INTO country(country, party, url, position)
                VALUES(?,?,?,?) '''
        
        cur = conn.cursor()
        cur.execute(sql, country)
        conn.commit()
    
    except sqlite3.Error as error:
        print('Error occurred - ', error)
    
    finally:
        if conn:
            conn.close()
            print('SQLite Connection closed')
    
    return cur.lastrowid

if __name__ == '__main__':
    create_write_dict_db('test', {'Field1': 'bla', 'Field2': 2, 'Field3': 3.141}, verbose=True)