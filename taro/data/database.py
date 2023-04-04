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
            
def create_write_dict_db(table_name: str, data: list, verbose = False):
    """
    Writes the contents of a dictionary into a table in the database
    ! DESTRUCTIVE: overwrites pre-existing table of same name
    """
    sqliteConnection = None
    try:
    
        # Connect to databse
        sqliteConnection = sqlite3.connect(database=os.getenv("DB_PATH"))
        cursor = sqliteConnection.cursor()


        ## If table already exists, back it up
        
        # Check if table exists
        try:
            listOfTables = cursor.execute(
                f"""SELECT tbl_Name FROM sqlite_master WHERE type='table'
                AND tbl_Name='{table_name}'; """).fetchall()
            
            # if exists, create backup copy        
            if listOfTables != []:
                cursor.execute(f"CREATE TABLE {table_name}_BACKUP as SELECT * FROM {table_name}")
            
            # Drop old table of same name
            cursor.execute(f"drop table if exists {table_name}")
        except:
            pass
        
        try:   
            # create field names for table from dictionary keys
            data_types = {'int': 'INTEGER', 'float': 'REAL', 'str': 'TEXT'}
            
            field_names = [f'{key} {data_types[type(value).__name__]}' for key, value in data[0].items()]
            field_names = ', '.join(field_names)
            
            # Create table 
            cursor.execute(f'create table {table_name} ({field_names});') 
            
            ## Insert data into table
            # Pepare keys
            keys = ', '.join(data[0].keys())
            
            # prepare values as list of tuples
            values = [ tuple([str(value) for value in data_dict.values()]) for data_dict in data ]
            
            # insert all 
            cursor.executemany(f"insert into {table_name} ({keys}) VALUES ({('?, '*len(values)).strip(', ')});", values)
        
            # Show student table
            if verbose:
                cursor.execute(f'select * from {table_name};')
        
                # View result
                result = cursor.fetchall()
                print(result)
        
            # Commit work and close connection
            sqliteConnection.commit()
            cursor.close()
        
        # If error occurs during writing into table, restore with backup if exists
        except sqlite3.Error as error:
            print(f'ERROR: {error}')
            listOfTables = cursor.execute(
                f"""SELECT tbl_Name FROM sqlite_master WHERE type='table'
                AND tbl_Name='{table_name}_BACKUP'; """).fetchall()
            
            try:
                cursor.execute(f"DROP TABLE {table_name};")
            except:
                pass
            
            if listOfTables != []:
                cursor.execute(f"CREATE TABLE {table_name} as SELECT * FROM {table_name}_BACKUP")
                
                cursor.execute(f"DROP TABLE {table_name}_BACKUP;")
            
            
                
            
    
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
    data = [{'Field1': 'bla', 'Field2': 2, 'Field3': 3.141}, {'Field1': 'blafdf', 'Field2': 42, 'Field3': 3.1431}, {'Field1': 'blfsa', 'Field2': 4, 'Field3': 3.431}]
    create_write_dict_db('test', data, verbose=True)