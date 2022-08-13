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
    print("Sucessfuly connected to the databse")
    return cur, conn

def create_tables(cur):
    '''
    Create table based on the ddl statement
    '''
    for drop_table in drop_tables_list:
        cur.execute(drop_table)

    for create_table in create_table_list:
        cur.execute(create_table)
        print("Table created")

def print_schema(cur):  
    '''
    Print the schema of the tables created. To make sure it`s correct
    '''

    print("----------------SCHEMA----------------")
    for table in tables_names_list:
        sql_print_table = "SELECT * FROM "+table+" LIMIT 0"
        cur.execute(sql_print_table)
        colnames = [desc[0] for desc in cur.description]
        
        print(colnames)

def ingestion(cur):
    tables_list = ["products"]
    for table in tables_list:
        current = os.getcwd()
        datafolder = f"data/{table}.csv"
        filepath = os.path.join (current, datafolder)
    

        sql = f"COPY {table} FROM STDIN DELIMITER ',' CSV HEADER"
        cur.copy_expert(sql, open(filepath, "r"))

def tester (cur):
    '''
    Query data from a table an print it, to make sure it was loaded properly
    '''

    print("-----Testing: querying data from tables-----")
    cur.execute("SELECT * FROM products")
    row = cur.fetchone()
    while row:
        print(row)
        row = cur.fetchmany()
    print("Done testing")

def main():
    cur, conn = create_connection()
    create_tables(cur)
    print_schema(cur)
    ingestion(cur)
    tester(cur)




if __name__ == '__main__':
    main()
