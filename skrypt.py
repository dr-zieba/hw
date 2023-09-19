import sqlite3
from sqlite3 import Error

db_name = "data.db"
table_name = "Customer"


# Create database
def database_connection(db_file):
    """create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def sql_fetch_all_data(db_file, table):
    """fetches all data from given table"""
    with database_connection(db_file) as con:
        try:
            cursor = con.cursor()
            cursor.execute(f"SELECT customerid, name, amount from {table};")
            result = cursor.fetchall()
            for item in result:
                print(f"{item}")
            return result
        except Exception as e:
            print(e)


def sql_show_all_tables():
    """Prints all tables in data base"""
    with database_connection(db_file=db_name) as con:
        try:
            cursor = con.cursor()
            con.execute(f"SELECT name FROM sqlite_master;")
            result = cursor.fetchall()
            for item in result:
                print(f"{item}")
        except Exception as e:
            print(e)


def get_user_data(cursor, customer_id, table_name):
    data = cursor.execute(
        f"SELECT amount from {table_name} where customerid={customer_id};"
    )
    return data.fetchone()


def add(db_file, customer_id, amount_to_add, table_name):
    """Add value to amount column for a user"""
    with database_connection(db_file) as con:
        try:
            cursor = con.cursor()
            current_amount = get_user_data(cursor, customer_id, table_name)
            if current_amount is None:
                raise ValueError("Customer does not exist")
            updated_amount = current_amount[0] + amount_to_add
            cursor.execute(
                f"UPDATE {table_name} set amount={updated_amount} where customerid={customer_id};"
            )
            print(
                f"""User amount before change: {current_amount[0]}
            User amount after change: {updated_amount}
            """
            )
            user_input = input("Do you want to commit the changes? y/n")
            if user_input.lower() == "y":
                con.commit()
            else:
                con.rollback()
                print("Changes wont be committed")

        except Exception as e:
            print(e)


def subtract(db_file, customer_id, amount_to_substract, table_name):
    """Subtracts value from amount for a user"""
    with database_connection(db_file) as con:
        try:
            cursor = con.cursor()
            current_amount = get_user_data(cursor, customer_id, table_name)
            if current_amount is None:
                raise ValueError("Customer does not exist")
            if amount_to_substract > current_amount[0]:
                raise ValueError(
                    "Subtract amount can not be higher then current user amount"
                )
            updated_amount = current_amount[0] - amount_to_substract
            cursor.execute(
                f"UPDATE {table_name} set amount = {updated_amount} where customerid={customer_id};"
            )
            print(
                f"""User amount before change: {current_amount[0]}
                User amount after change: {updated_amount}
                """
            )
            user_input = input("Do you want to commit the changes? y/n")
            if user_input == "y":
                con.commit()
            else:
                con.rollback()
                print("Changes wont be committed")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    while True:
        sql_fetch_all_data(db_name, "Customer")
        user_input = int(
            input(
                """What's your action ?: 
        1: Add
        2: Subtract
        3: Exit
        """
            )
        )
        if user_input == 3:
            exit()

        customer_id_input = int(input("Insert customer ID: "))
        amount_input = int(input("Insert amount: "))

        if user_input == 1:
            add(db_name, customer_id_input, amount_input, table_name)
        elif user_input == 2:
            subtract(db_name, customer_id_input, amount_input, table_name)