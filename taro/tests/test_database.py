from taro.data.database import create_write_dict_db
import psycopg2
import os


def test_db_connection():
    connection = None
    try:
    
        # Connect to databse
        connection = psycopg2.connect(dbname=os.getenv("POSTGRES_DB_NAME"),
                                user=os.getenv("POSTGRES_USER"),
                                password=os.getenv("POSTGRES_PASSWORD"),
                                host=os.getenv("POSTGRES_HOST"),
                                port=os.getenv("POSTGRES_PORT"))
        cursor = connection.cursor()
        
    finally:
        if connection:
            connection.close()
            print('Postgres Connection closed: test_clean_db')
            
            
def test_clean_db():
    connection = None
    try:
    
        # Connect to databse
        connection = psycopg2.connect(dbname=os.getenv("POSTGRES_DB_NAME"),
                                user=os.getenv("POSTGRES_USER"),
                                password=os.getenv("POSTGRES_PASSWORD"),
                                host=os.getenv("POSTGRES_HOST"),
                                port=os.getenv("POSTGRES_PORT"))
        cursor = connection.cursor()
    
        # fetch dummy table
        try:
            cursor.execute(f'DROP TABLE dummy;')
        except:
            pass
        try:
            cursor.execute(f'DROP TABLE dummy_BACKUP;')
        except:
            pass
        
    finally:
        if connection:
            connection.close()
            print('Postgres Connection closed: test_clean_db')

def test_dummy_table():
    
    # create dummy data
    data = [{'Field1': 'bla', 'Field2': 2, 'Field3': 3.141}, {'Field1': 'blafdf', 'Field2': 42, 'Field3': 3.1431}, {'Field1': 'blfsa', 'Field2': 4, 'Field3': 3.431}]
    
    # Write dummy data to db
    create_write_dict_db('dummy', data)
    
    
    connection = None
    try:
    
        # Connect to databse
        connection = psycopg2.connect(dbname=os.getenv("POSTGRES_DB_NAME"),
                                user=os.getenv("POSTGRES_USER"),
                                password=os.getenv("POSTGRES_PASSWORD"),
                                host=os.getenv("POSTGRES_HOST"),
                                port=os.getenv("POSTGRES_PORT"))
        cursor = connection.cursor()
    
        # fetch dummy table
        cursor.execute(f'select * from dummy;')
        result = cursor.fetchall()
        
        assert result == [('bla', 2, 3.141), ('blafdf', 42, 3.1431), ('blfsa', 4, 3.431)]
        
    finally:
        if connection:
            connection.close()
            print('Postgres Connection closed: test_dummy_table')
    
# def test_dummy_backup():
#     pass
#     # create dummy data
#     new_data = [{'Field1': 'blub', 'Field2': 3, 'Field3': 3.1421, 'Field4': True}, {'Field1': 'blafdf', 'Field2': 42, 'Field3': 3.1431, 'Field22': 3.222}, {'Field1': 'blfsa', 'Field2': 4, 'Field3': 3.431}]
    
#     # Write dummy data to db
#     create_write_dict_db('dummy', new_data)
    
#     connection = None
#     try:
    
#         # Connect to databse
#         connection = psycopg2.connect(dbname=os.getenv("POSTGRES_DB_NAME"),
#                                 user=os.getenv("POSTGRES_USER"),
#                                 password=os.getenv("POSTGRES_PASSWORD"),
#                                 host=os.getenv("POSTGRES_HOST"),
#                                 port=os.getenv("POSTGRES_PORT"))
#         cursor = connection.cursor()
    
#         # fetch dummy table
#         cursor.execute(f'select * from dummy_BACKUP;')
#         result = cursor.fetchall()
        
#         assert result == [('bla', 2, 3.141), ('blafdf', 42, 3.1431), ('blfsa', 4, 3.431)]
        
#     finally:
#         if connection:
#             connection.close()
#             print('Postgres Connection closed: test_dummy_backup')
            
                
def test_dummy_backup_restore():
    
    # Create bad data
    bad_data = [{'Field1': 'blub', 'Field2': 3, 'Field3': 'BAD_DATA', "Field4": True}, {'Field1': 'blafdf', 'Field2': 42, 'Field3': 3.1431}, {'Field1': 'blfsa', 'Field2': 4, 'Field3': 3.431}]

    # Write bad dummy data to db
    create_write_dict_db('dummy', bad_data)
    
    try:

        # Connect to databse
        connection = psycopg2.connect(dbname=os.getenv("POSTGRES_DB_NAME"),
                                user=os.getenv("POSTGRES_USER"),
                                password=os.getenv("POSTGRES_PASSWORD"),
                                host=os.getenv("POSTGRES_HOST"),
                                port=os.getenv("POSTGRES_PORT"))
        cursor = connection.cursor()
    
        # fetch dummy table
        cursor.execute(f'select * from dummy;')
        result = cursor.fetchall()
        
        assert result == [('bla', 2, 3.141), ('blafdf', 42, 3.1431), ('blfsa', 4, 3.431)]
        
    finally:
        if connection:
            connection.close()
            print('Postgres Connection closed: test_dummy_backup_restore')
            
def test_dummy_backup_drop():
    
    try:

        # Connect to databse
        connection = psycopg2.connect(dbname=os.getenv("POSTGRES_DB_NAME"),
                                user=os.getenv("POSTGRES_USER"),
                                password=os.getenv("POSTGRES_PASSWORD"),
                                host=os.getenv("POSTGRES_HOST"),
                                port=os.getenv("POSTGRES_PORT"))
        cursor = connection.cursor()
    
        # fetch dummy table
        cursor.execute(f"SELECT tablename FROM pg_tables WHERE tablename='dummy_backup'")
        result = cursor.fetchall()
        
        print(result)
        
        assert result == []
        
    finally:
        if connection:
            connection.close()
            print('Postgres Connection closed: test_dummy_backup_restore')