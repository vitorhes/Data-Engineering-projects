tables_names_list = ["products", "accounts", "transactions"]



accounts_drop_table = ("""
 DROP TABLE IF EXISTS accounts;
""")
accounts_table_create = ("""
    CREATE TABLE IF NOT EXISTS accounts
        (
            customer_id INTEGER PRIMARY KEY,
            first_name VARCHAR,
            last_name VARCHAR,
            address_1 VARCHAR,
            address_2 VARCHAR,  
            city VARCHAR,
            state VARCHAR,
            zip_code VARCHAR,
            join_date VARCHAR
            
        );
""")


products_drop_table = ("""
 DROP TABLE IF EXISTS products;
""")
products_table_create = ("""
    CREATE TABLE IF NOT EXISTS products
        (
            product_id INTEGER PRIMARY KEY,
            product_code INTEGER NOT NULL,
            product_description VARCHAR
        );
""")


transactions_drop_table = ("""
 DROP TABLE IF EXISTS transactions;
""")

transactions_table_create = ("""
    CREATE TABLE IF NOT EXISTS transactions
        (
            transaction_id VARCHAR PRIMARY KEY,
            transaction_date VARCHAR,
            product_id INTEGER,
            product_code INTEGER,
            product_description VARCHAR,  
            quantity INTEGER,
            account_id INTEGER
        );
""")


drop_tables_list = [products_drop_table,accounts_drop_table,transactions_drop_table]
create_table_list = [products_table_create,accounts_table_create,transactions_table_create]
