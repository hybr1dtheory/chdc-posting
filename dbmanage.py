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
    
    def get_locations_set(self, lang="uk") -> set:
        """Returns a set of tuples with full locations 
        (oblast, raion, hromada, settlement), only if dict_rows=False,
        else raises an exception. Parameter lang must be str witn language code:
        'uk' (default) - names in Ukrainian,
        'en' - names in English (trasliteration)."""
        match lang:
            case "uk":
                self.__cur.execute(f"""
                    SELECT o.name_ua, r.name_ua, h.name_ua, s.name_ua
                    FROM oblast o
                    JOIN raion r ON o.id = r.oblast_id
                    JOIN hromada h ON r.id = h.raion_id
                    JOIN settlement s ON h.id = s.hromada_id
                """)
            case "en":
                self.__cur.execute(f"""
                    SELECT o.name_en, r.name_en, h.name_en, s.name_en
                    FROM oblast o
                    JOIN raion r ON o.id = r.oblast_id
                    JOIN hromada h ON r.id = h.raion_id
                    JOIN settlement s ON h.id = s.hromada_id
                """)
            case _:
                raise ValueError(
                    f"lang must be str language code 'uk' or 'en', not {lang}"
                    )
        return set(self.__cur.fetchall())
