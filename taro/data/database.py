import psycopg2
import os
from psycopg2 import Error

def create_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = psycopg2.connect(dbname=os.getenv("POSTGRES_DB_NAME"),
                                user=os.getenv("POSTGRES_USER"),
                                password=os.getenv("POSTGRES_PASSWORD"),
                                host=os.getenv("POSTGRES_HOST"),
                                port=os.getenv("POSTGRES_PORT"))
        print(psycopg2.__version__)
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
    connection = None
    try:
    
        print(os.getenv('POSTGRES_HOST') + +':'+os.getenv('POSTGRES_PORT'))
        # Connect to databse
        connection = psycopg2.connect(dbname=os.getenv("POSTGRES_DB_NAME"),
                                user=os.getenv("POSTGRES_USER"),
                                password=os.getenv("POSTGRES_PASSWORD"),
                                host=os.getenv("POSTGRES_HOST"),
                                port=os.getenv("POSTGRES_PORT"))
        cursor = connection.cursor()


        ## If table already exists, back it up
        
        # Check if table exists
        try:
            
            cursor.execute(
                f"""SELECT tablename FROM pg_tables WHERE tablename='{table_name}'; """)
            listOfTables = cursor.fetchall()

            
            # if exists, create backup copy        
            if listOfTables != []:
                cursor.execute(f"drop table if exists {table_name}_backup")
                cursor.execute(f"CREATE TABLE {table_name}_backup as SELECT * FROM {table_name}")
            
            # Drop old table of same name
            cursor.execute(f"drop table if exists {table_name}")
            
        except psycopg2.Error as error:
            print('Error occurred while trying to create backup - ', error)
        
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
            
            # DEBUG
            #for value in values:
            #    print(value)
            
            # insert all 
            cursor.executemany(f"insert into {table_name} ({keys}) VALUES ({('%s, '*len(data[0].keys())).strip(', ')});", values)
        
            # Show table table
            if verbose:
                cursor.execute(f'select * from {table_name};')
        
                # View result
                result = cursor.fetchall()
                print(result)
        
            # Commit work and close connection
            connection.commit()
            cursor.close()
        
        # If error occurs during writing into table, restore with backup if exists
        except BaseException as error:
            print(f'ERROR: {error}')
            
            # Get backup table
            cursor.execute(
                f"""SELECT tablename FROM pg_tables WHERE tablename='{table_name}_backup'; """)
            listOfTables = cursor.fetchall()
            
            print('listofTables: ' + str(len(listOfTables)))
            
            # Drop corrupted table if exists
            cursor.execute(f"drop table if exists {table_name}")
            
            # If backup exists, restore from it and then drop
            if listOfTables != []:
                
                print('Restoring table')
                cursor.execute(f"CREATE TABLE {table_name} as SELECT * FROM {table_name}_backup")
                
                print('Dropping Backup Table')
                cursor.execute(f"DROP TABLE {table_name}_backup;")
                
            connection.commit()
            cursor.close()
            
            
                
            
    
    except psycopg2.Error as error:
        print('Error occurred while trying to connect - ', error)
    
    finally:
        if connection:
            connection.close()
            print('Postgres Connection closed')

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
    data = [{'Field1': 'bla', 'Field2': 2, 'Field3': 3.141}, {'Field1': 'bla', 'Field2': 2, 'Field3': 3.141}, {'Field1': 'blafdf', 'Field2': 42, 'Field3': 3.1431}, {'Field1': 'blfsa', 'Field2': 4, 'Field3': 3.431}]
    create_write_dict_db('test', data, verbose=True)