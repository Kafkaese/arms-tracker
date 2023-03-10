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
        
        # Create country table 
        cursor.execute(f'create table {table_name} ({field_names});') 
    
        # create field names for table from dictionary keys
        data_types = {'int': 'INTEGER', 'float': 'REAL', 'str': 'TEXT'}
        
        field_names = [f'{key} {data_types[type(value).__name__]}' for key, value in data.items()]
        field_names = ', '.join(field_names)
        
        
    
        # Insert data into table
        #cursor.executemany("insert into country (country, party, url, position) VALUES (?, ?, ?, ?);", country_info)
    
        # Show student table
        #if verbose:
        #    cursor.execute('select * from country;')
    
        # View result
        #result = cursor.fetchall()
        #print(result)
    
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
    create_write_dict_db('test', {'Field1': 'bla', 'Field2': 2, 'Field3': 3.141})