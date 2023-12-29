import sqlite3


def create_connection(db_name):
    connection = None
    try:
        connection = sqlite3.connect(db_name)
        print(f"Connected to SQLite database '{db_name}' successfully!")
    except sqlite3.Error as e:
        print(e)
    return connection


def create_products_table(connection):
    sql_create_products_table = '''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_title VARCHAR(200) NOT NULL,
        category VARCHAR(50) NOT NULL,
        price REAL NOT NULL DEFAULT 0.0,
        quantity INTEGER NOT NULL DEFAULT 0
    )
    '''
    create_table(connection, sql_create_products_table)

def add_columns_to_products(connection):
    pass

def add_sample_products(connection):
    products = [
        ('Tomato', 'Vegetables', 1.5, 20),
        ('Cucumber', 'Vegetables', 1.0, 30),
        ('Carrot', 'Vegetables', 0.8, 25),
        ('Milk', 'Dairy', 2.0, 15),
        ('Cheese', 'Dairy', 3.5, 10),
        ('Yogurt', 'Dairy', 1.2, 12),
        ('Apple', 'Fruits', 2.0, 18),
        ('Banana', 'Fruits', 1.5, 22),
        ('Orange', 'Fruits', 1.8, 20),
        ('Broccoli', 'Vegetables', 2.5, 15),
        ('Eggplant', 'Vegetables', 1.2, 18),
        ('Mango', 'Fruits', 3.0, 12),
        ('Butter', 'Dairy', 2.8, 10),
        ('Spinach', 'Vegetables', 1.2, 20),
        ('Strawberry', 'Fruits', 2.5, 15),
    ]

    for product in products:
        insert_product(connection, product)


def update_quantity_by_id(connection, product_id, new_quantity):
    sql_update_quantity = '''UPDATE products SET quantity = ? WHERE id = ?'''
    execute_sql_query(connection, sql_update_quantity, (new_quantity, product_id))


def update_price_by_id(connection, product_id, new_price):
    sql_update_price = '''UPDATE products SET price = ? WHERE id = ?'''
    execute_sql_query(connection, sql_update_price, (new_price, product_id))


def delete_product_by_id(connection, product_id):
    sql_delete_product = '''DELETE FROM products WHERE id = ?'''
    execute_sql_query(connection, sql_delete_product, (product_id,))


def select_all_products(connection):
    sql_select_all = '''SELECT * FROM products'''
    rows_list = execute_sql_query(connection, sql_select_all)
    print("All Products:")
    print_products(rows_list)


def select_products_below_price_limit(connection, price_limit, quantity_limit):
    sql_select_below_limit = '''SELECT * FROM products WHERE price < ? AND quantity > ?'''
    params = (price_limit, quantity_limit)
    rows_list = execute_sql_query(connection, sql_select_below_limit, params)
    print(f"Products below price limit ({price_limit} som) and above quantity limit ({quantity_limit} units):")
    print_products(rows_list)


def search_products_by_title(connection, search_term):
    sql_search_by_title = '''SELECT * FROM products WHERE product_title LIKE ?'''
    params = ('%' + search_term + '%',)
    rows_list = execute_sql_query(connection, sql_search_by_title, params)
    print(f"Search results for '{search_term}':")
    print_products(rows_list)


def test_functions():
    db_connection = create_connection("hw.db")
    create_products_table(db_connection)


    clear_table(db_connection)

    add_sample_products(db_connection)

    select_all_products(db_connection)

    update_quantity_by_id(db_connection, 3, 50)
    update_price_by_id(db_connection, 5, 25.5)

    select_products_below_price_limit(db_connection, 2.0, 15)

    search_products_by_title(db_connection, "Tomato")

    delete_product_by_id(db_connection, 8)

    select_all_products(db_connection)

    db_connection.close()

def create_table(connection, sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
    except sqlite3.Error as e:
        print(e)


def execute_sql_query(connection, sql, params=None):
    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        rows_list = cursor.fetchall()
        connection.commit()
        return rows_list
    except sqlite3.Error as e:
        print(e)
        return None


def insert_product(connection, product):
    sql = '''INSERT INTO products (product_title, category, price, quantity) VALUES (?, ?, ?, ?)'''
    execute_sql_query(connection, sql, product)


def print_products(rows_list):
    for row in rows_list:
        print(row)


def clear_table(connection):
    sql_clear_table = '''DELETE FROM products'''
    execute_sql_query(connection, sql_clear_table)


test_functions()
