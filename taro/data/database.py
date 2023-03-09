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
            
def write_dicst_db(table_name: str, data: dict, verbose = False):
    
    
    try:
    
        # Connect to databse
        sqliteConnection = sqlite3.connect(database=os.getenv["DB_PATH"])
        cursor = sqliteConnection.cursor()
    
        # Create country table 
        cursor.execute('drop table %(table_name)s', {"table_name": table_name})
        cursor.execute('create table %(table_name)s(country TEXT, party TEXT, url TEXT, position TEXT);', {"table_name": table_name}) 
    
        # Insert data into table
        cursor.executemany(
            "insert into country (country, party, url, position) VALUES (?, ?, ?, ?);", country_info)
    
        # Show student table
        if verbose:
            cursor.execute('select * from country;')
    
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
