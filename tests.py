import unittest
import sqlite3
from unittest.mock import patch
from skrypt import database_connection, sql_fetch_all_data, add, subtract, get_user_data


class TestBazaDanych(unittest.TestCase):
    def setUp(self):
        # Tworzenie tymczasowej bazy danych w pamięci RAM
        self.conn = sqlite3.connect("test.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Customer (
                id INTEGER PRIMARY KEY,
                name TEXT,
                amount INTEGER,
                customerid INTEGER
            )
        """
        )
        self.cursor.execute(
            "INSERT INTO Customer (name, amount, customerid) VALUES (?, ?, ?)",
            ("Jan", 100, 1),
        )
        self.conn.commit()

    def tearDown(self):
        # Zamknięcie tymczasowego połączenia z bazą danych
        self.cursor.execute("DROP TABLE IF EXISTS Customer")
        self.conn.close()

    def test_sql_fetch_all_data(self):
        #test funckji sql_fetch_all_data
        data = sql_fetch_all_data("test.db", "Customer")
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][0], 1)
        self.assertEqual(data[0][1], "Jan")
        self.assertEqual(data[0][2], 100)

    @patch("builtins.input", side_effect=["y"])
    def test_add(self, mock_input):
        # test funckji add
        add("test.db", 1, 100, "Customer")
        result = get_user_data(self.cursor, 1, "Customer")
        self.assertEqual(result[0], 200)

    def test_add_user_doesnot_exists(self):
        with self.assertRaises(Exception) as context:
            add("test.db", 99, 100, "Customer")
            self.assertIn("Customer does not exist", str(context.exception))

    @patch("builtins.input", side_effect=["y"])
    def test_subtract(self, mock_input):
        # test funckji test_subtract
        subtract("test.db", 1, 10, "Customer")
        result = get_user_data(self.cursor, 1, "Customer")
        self.assertEqual(result[0], 90)

    def test_subtract_user_doesnot_exists(self):
        with self.assertRaises(Exception) as context:
            subtract("test.db", 99, 10, "Customer")
            self.assertIn("Customer does not exist", str(context.exception))

    def test_subtract_amount_too_high(self):
        with self.assertRaises(Exception) as context:
            subtract("test.db", 1, 1000, "Customer")
            self.assertIn(
                "Subtract amount can not be higher then current user amount",
                str(context.exception),
            )


if __name__ == "__main__":
    unittest.main()
