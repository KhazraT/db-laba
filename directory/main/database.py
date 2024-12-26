import psycopg2
from psycopg2.extensions import connection as Connection

def connect_to_database():
    connection = None
    try:
        connection = psycopg2.connect(
            host='127.0.0.1',
            user='postgres',
            password='1234',
            database='directory'
        )
        connection.autocommit = True
    except Exception as ex:
        print('[INFO] Error while working with PostrgreSQL:', ex)
    
    return connection

def create_tables(connection: Connection):
    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS fam(
                        F_NUM serial PRIMARY KEY,
                        F_VAL CHAR(20) UNIQUE
                       );
                       
                       CREATE TABLE IF NOT EXISTS name_(
                        n_num serial PRIMARY KEY,
                        Nam_val VARCHAR(20) UNIQUE
                       );
                       
                       CREATE TABLE IF NOT EXISTS otc(
                        Otc_n serial PRIMARY KEY,
                        Otc_val VARCHAR(20) UNIQUE
                       );
                       
                       CREATE TABLE IF NOT EXISTS street(
                        s_num serial PRIMARY KEY,
                        s_val VARCHAR(20) UNIQUE
                       );
                       
                       CREATE TABLE IF NOT EXISTS main(
                        id serial PRIMARY KEY,
                        FAM INTEGER REFERENCES fam ON DELETE RESTRICT,
                        NAME_ INTEGER REFERENCES name_ ON DELETE RESTRICT,
                        Sndname INTEGER REFERENCES otc ON DELETE RESTRICT,
                        Street INTEGER REFERENCES street ON DELETE RESTRICT,
                        Bldn VARCHAR(8),
                        Bldn_kor VARCHAR(8),
                        Appr INTEGER,
                        Telef CHAR(12) UNIQUE
                       );""")

def drop_table(connection: Connection):
    with connection.cursor() as cursor:
        cursor.execute("""DROP TABLE IF EXISTS main;
                       DROP TABLE IF EXISTS street;
                       DROP TABLE IF EXISTS otc;
                       DROP TABLE IF EXISTS name_;
                       DROP TABLE IF EXISTS fam;""")

def insert_into_sub_tables(connection: Connection, table, columns, value):
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO {table} ({columns}) VALUES ({value})""")

def delete_value_from_table(connection: Connection, table, condition):
    with connection.cursor() as cursor:
        cursor.execute(f"""DELETE FROM {table} WHERE {condition}""")

def select_from_sub_table(connection: Connection, table, columns="*", condition=None):
    with connection.cursor() as cursor:
        if condition == None:
            cursor.execute(f"""SELECT {columns} FROM {table}""")
        else:
            cursor.execute(f"""SELECT {columns} FROM {table} WHERE {condition}""")

        return cursor.fetchall()

def is_exists(connection: Connection, table, columns="*", condition=None):
    values = select_from_sub_table(connection, table, columns, condition)

    if len(values):
        return True
    return False

def close_connection(connection: psycopg2.connect):
    if connection:
        connection.cursor().close()
        connection.close()
        # print('[INFO] PostgreSQL connection closed')

def select_from_main_table(connection: Connection, condition=None):
    with connection.cursor() as cursor:
        if condition == None:
            cursor.execute("""SELECT id, fam.f_val, name_.nam_val, otc.otc_val, street.s_val, bldn, bldn_kor, appr, telef FROM 
                            main JOIN fam ON main.fam=fam.f_num 
                                JOIN name_ ON main.name_=name_.n_num
                                JOIN otc ON main.sndname=otc.otc_n
                                JOIN street ON main.street=street.s_num""")
        else:
            cursor.execute(f"""SELECT id, fam.f_val, name_.nam_val, otc.otc_val, street.s_val, bldn, bldn_kor, appr, telef FROM 
                            main JOIN fam ON main.fam=fam.f_num 
                                JOIN name_ ON main.name_=name_.n_num
                                JOIN otc ON main.sndname=otc.otc_n
                                JOIN street ON main.street=street.s_num WHERE {condition}""")
        return cursor.fetchall()

def insert_into_main(connection: Connection, table, values):
    with connection.cursor() as cursor:
        cursor.execute(f"""INSERT INTO {table} VALUES {values}""")

if __name__ == "__main__":
    connection = connect_to_database()
    create_tables(connection)
    # drop_table(connection)
    # connection.cursor().execute("""DELETE FROM otc WHERE otc_n=1""")
    close_connection(connection)