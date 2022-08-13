
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

drop_tables_list = [products_drop_table]
create_table_list = [products_table_create]
tables_names_list = ["products"]