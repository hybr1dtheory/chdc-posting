"""Classes and functions for managing SQlite3 database"""
import sqlite3


def dict_factory(cursor, row: tuple) -> dict:
    """Row factory returns each row as a dict
    (key = column name, value = row value for the column)"""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


class DBManager:
    """Class with methods to get data from database."""
    def __init__(self, db_name: str, dict_rows=False) -> None:
        """If dict_rows=True methods will return a list of dicts."""
        self.__con = sqlite3.connect(db_name)
        if dict_rows:
            self.__con.row_factory = dict_factory
        self.__cur = self.__con.cursor()
    
    # def __enter__(self):
        # return self
    
    # def __exit__(self):
        # self.__con.close()
    
    def select(self, table_name: str, columns: tuple[str] | None = None) -> list[dict] | list[tuple]:
        """Method to get all rows from selected columns of the table <table_name>.
        If no columns metod selects all columns (*)."""
        if columns:
            self.__cur.execute(f"SELECT {', '.join(columns)} FROM {table_name}")
            return self.__cur.fetchall()
        self.__cur(f"SELECT * FROM {table_name}")
        return self.__cur.fetchall()
    
    def where_eq(self, table_name: str, conditions: dict,
                columns: tuple[str] | None = None) -> list[dict] | list[tuple]:
        """Method to get rows from selected columns of the table <table_name>,
        where key == value in conditions dict (key must be a valid column name).
        If no columns metod selects all columns (*)."""
        where = [f"{k} = '{v}'" for k, v in conditions.items()]
        if columns:
            self.__cur.execute(f"""
                SELECT {', '.join(columns)}
                FROM {table_name}
                WHERE {' AND '.join(where)};
            """)
            return self.__cur.fetchall()
        self.__cur.execute(f"""
            SELECT *
            FROM {table_name}
            WHERE {' AND '.join(where)};
        """)
        return self.__cur.fetchall()
    
    def get_translit_dict(self, table_name: str) -> dict:
        """Returns dict with ukrainian names as keys 
        and latin trasliteration as values"""
        self.__cur.execute(f"""
            SELECT name_ua, name_en
            FROM {table_name};
        """)
        res = self.__cur.fetchall()
        if res:
            if isinstance(res[0], tuple):
                return dict(res)
            elif isinstance(res[0], dict):
                return dict([tuple(r.values()) for r in res])
        return {}
