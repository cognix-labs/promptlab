import sqlite3
from typing import Dict, List, Tuple


class SQLiteClient:
    def __init__(self, db_file: str):
        """Initialize the SQLiteHelper with a database name."""
        self.db_file = db_file

    @staticmethod
    def dict_factory(cursor: sqlite3.Cursor, row: tuple) -> Dict:
        """Convert database row to dictionary"""
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    def create_connection(self):
        """Create and return a database connection."""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = self.dict_factory

        return conn

    def execute_query(self, query: str, params: Tuple = ()):
        """Execute a query such as CREATE TABLE or INSERT."""
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(
                    "An asset (dataset/prompt) or an experiment with this name/ID already exists"
                    "Please use unique names/IDs for each asset/experiment."
                ) from e
            raise
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()
            conn.close()

    def execute_query_many(self, query: str, params: List[Tuple]):
        """Execute a query such as CREATE TABLE or INSERT."""
        conn = self.create_connection()
        cursor = conn.cursor()
        try:
            cursor.executemany(query, params)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()
            conn.close()

    def fetch_data(self, query: str, params: Tuple = ()) -> list:
        """Fetch data from the database using a SELECT query."""
        conn = self.create_connection()
        cursor = conn.cursor()
        result = []
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            cursor.close()
            conn.close()
        return result
