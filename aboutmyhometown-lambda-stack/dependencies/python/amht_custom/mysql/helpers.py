"""helpers - This module contains the helper methods to make using the mysql
connector a little simpler
"""

import logging
from typing import List, Tuple

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection, CMySQLConnection

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _construct_delete(
    table_name: str,
    where: str,
):
    """Constructs a textual delete statement given a table and a where"""
    if not where:
        raise ValueError("Delete too broad!")
    if not any(char in where for char in [">", "<", "="]):
        raise ValueError("Delete too broad!")
    return f"DELETE FROM {table_name} WHERE {where}"


def _construct_insert_from_columns(
    table_name: str,
    column_names: List[str],
    keys_to_update: Tuple = (),
):
    """Constructs a textual insert statement given a list of columns and a table name"""
    return (
        f"INSERT INTO `{table_name}` "
        f"({', '.join([f'`{name}`' for name in column_names])}) VALUES "
        f"({', '.join(['%s' for _ in column_names])}) "
        f"""{f"ON DUPLICATE KEY UPDATE {', '.join([f'`{key}` = VALUES(`{key}`)' for key in keys_to_update])}" if keys_to_update else ''}"""  # pylint: disable=line-too-long
    )


def construct_inserts_from_dicts(
    table_name: str,
    list_of_rowdicts: List[dict],
    database_connection: PooledMySQLConnection | MySQLConnection | CMySQLConnection,
    keys_to_update: Tuple = (),
    on_duplicate_skip: bool = False,
) -> Tuple[str, List[tuple]]:
    """Constructs the SQL executemany format of a list of tuples and the insert
        statements

    Parameters
    ----------
        table_name: str
            The name of the table to insert into
        list_of_rowdicts: List[dict]
            The list of rows as dictionaries to insert
        database_connection: PooledMySQLConnection | MySQLConnection | CMySQLConnection
            The database connector to use
        keys_to_update: Tuple
            A tuple of keys to update on duplicate inserts.
            Has no default. Takes priority over 'on_duplicate_skip'.
        on_duplicate_skip: bool
            Whether or not to skip duplicate values
            Uses 'on duplicate key update' primary keys

    Return
    ----------
        str
            The textual insert statement
        List[tuple]
            The list of row values to insert
    """
    with database_connection.cursor() as cursor:
        cursor.execute(
            "SELECT column_name, CASE WHEN column_key = 'PRI' THEN 1 ELSE 0 END "
            f"as is_primary FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
        )
        results = cursor.fetchall()
        column_names = [name for name, _ in results]
        primary_keys = tuple(name for name, primary in results if primary)

    all_column_names = []
    all_values = []
    for row in list_of_rowdicts:
        for column in row:
            if column not in column_names:
                raise AttributeError(f"Table '{table_name}' has no column '{column}'")
            if column not in all_column_names:
                all_column_names.append(column)

    for row in list_of_rowdicts:
        cur_value_list = []
        for column in all_column_names:
            cur_value_list.append(row.get(column, None))
        all_values.append(tuple(cur_value_list))

    if on_duplicate_skip and not keys_to_update:
        keys_to_update = primary_keys

    insert_stmt = _construct_insert_from_columns(
        table_name=table_name,
        column_names=all_column_names,
        keys_to_update=keys_to_update,
    )

    return insert_stmt, all_values


def insert_many_dict(
    table_name: str,
    list_of_rowdicts: List[dict],
    database_connection: PooledMySQLConnection | MySQLConnection | CMySQLConnection,
    keys_to_update: Tuple = tuple(),
    on_duplicate_skip: bool = False,
) -> int:
    """Insert into the sql database provided based on a list of dictionaries
        representing rows

    Parameters
    ----------
        table_name: str
            The name of the table to insert into
        list_of_rowdicts: List[dict]
            The list of rows as dictionaries to insert
        database_connection: PooledMySQLConnection | MySQLConnection | CMySQLConnection
            The database connector to use
        keys_to_update: Tuple
            A tuple of keys to update on duplicate inserts.
            Has no default. Takes priority over 'on_duplicate_skip'.
        on_duplicate_skip: bool
            Whether or not to skip duplicate values.
            Uses 'on duplicate key update' primary keys

    Return
    ----------
        int
            Number of rows succesfully inserted

    Examples
    ----------
    >>> from datetime import datetime
    >>> rows_to_insert = [
    ...     {
    ...         "int": 5,
    ...         "date": datetime.now(),
    ...         "varchar": "This is a varchar",
    ...     },
    ...     {
    ...         "int": 4,
    ...         "date": datetime.now(),
    ...         "varchar": "This is also a varchar",
    ...     },
    ...     {
    ...         "int": 1,
    ...         "date": datetime.now(),
    ...         "varchar": "Similarly a varchar",
    ...     },
    ... ]

    >>> try:
    ...     insert_many_dict("simple", rows_to_insert, database_connection)
    ... except Exception:
    ...     print("Failed because testing")
    Failed because testing
    """
    logger.debug(
        "Inserting %s dictionaries into table `%s`", len(list_of_rowdicts), table_name
    )

    insert_stmt, all_values = construct_inserts_from_dicts(
        table_name=table_name,
        list_of_rowdicts=list_of_rowdicts,
        database_connection=database_connection,
        keys_to_update=keys_to_update,
        on_duplicate_skip=on_duplicate_skip,
    )

    logger.debug("Generated INSERT statement: %s", insert_stmt)

    with database_connection.cursor() as cursor:
        cursor.executemany(insert_stmt, all_values)

    if cursor.rowcount > 0:
        database_connection.commit()

    logger.debug("Inserted %s rows", cursor.rowcount)

    return cursor.rowcount


def delete_after_time(
    table_name: str,
    database_connection: PooledMySQLConnection | MySQLConnection | CMySQLConnection,
    column_name: str = "dbinsert",
    days: int = 90,
    where: str | None = None,
) -> int:
    """Insert into the sql database provided based on a list of dictionaries
        representing rows

    Parameters
    ----------
        table_name: str
            The name of the table to insert into
        database_connection: PooledMySQLConnection | MySQLConnection | CMySQLConnection
            The database connector to use
        column_name: str
            The name of the column whose date should be checked (default "dbinsert")
        days: int
            The number of days to retain logs from (default 90)
        where: str
            Allows you to add aditional elements to the where clause (default None)

    Return
    ----------
        int
            Number of rows succesfully deleted

    Examples
    ----------
    >>> try:
    ...     delete_after_time("simple", database_connection)
    ... except Exception:
    ...     print("Failed because testing")
    Failed because testing
    """
    logger.debug("Deleting from %s", table_name)
    all_where = f"{column_name} < DATE_SUB(NOW(), INTERVAL {days} DAY)"

    if where:
        all_where = f"{all_where} AND {where}"

    delete_stmt = _construct_delete(
        table_name=table_name,
        where=all_where,
    )

    logger.debug("Generated DELETE statement: %s", delete_stmt)

    with database_connection.cursor() as cursor:
        cursor.execute(delete_stmt)

    if cursor.rowcount > 0:
        database_connection.commit()

    logger.debug("Deleted %s rows", cursor.rowcount)

    return cursor.rowcount
