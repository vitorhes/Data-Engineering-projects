import psycopg2
from asyncio import create_task
from createstatements import *
import os


def create_connection():
    host = 'postgres'
    database = 'postgres'
    user = 'postgres'
    pas = 'postgres'
    conn = psycopg2.connect(host=host, database=database, user=user, password=pas)
    cur = conn.cursor()
    conn.set_session(autocommit = True)
    print("-------Sucessfuly connected to the database-------")
    return cur, conn

def create_tables(cur):
    '''
    Drop every table, then recreate them based the ddl statement
    '''
    for drop_table in drop_tables_list:
        cur.execute(drop_table)

    for create_table in create_table_list:
        cur.execute(create_table)


def data_ingestion(cur):
    '''
    Ingest data from csv files located in data folder
    '''
    for table in tables_names_list:
        current = os.getcwd()
        datafolder = f"data/{table}.csv"
        filepath = os.path.join (current, datafolder)

        sql = f"COPY {table} FROM STDIN DELIMITER ',' CSV HEADER"
        cur.copy_expert(sql, open(filepath, "r"))

def tester (cur):
    '''
    Query data from a table and print it, to test if it was loaded properly
    '''
    for table in tables_names_list:
        print(f"-----Testing: querying data from {table}-----")
        cur.execute(f"SELECT * FROM {table}")
        row = cur.fetchall()
        while row:
            print(row)
            row = cur.fetchmany()
    print("Done testing")

def main():
    cur, conn = create_connection()
    create_tables(cur)
    data_ingestion(cur)
    tester(cur)


if __name__ == '__main__':
    main()
