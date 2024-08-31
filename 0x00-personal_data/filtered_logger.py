#!/usr/bin/env python3
'''
defines user hadling functions
'''
import mysql.connector
import csv
import re
from typing import List, Tuple
import logging
import os


# f'((?<={field}=)([^;])*(?={separator}))'
PII_FIELDS = ('name', 'ssn', 'email', 'phone', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''returns the log message obfuscated'''
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
        method to filter values in incoming log records using filter_datum
        '''
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    '''
    get_logger function that takes no arguments
    and returns a logging.Logger object
    '''
    my_logger = logging.getLogger("user_data")
    my_logger.propagate = False
    my_logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(formatter)
    my_logger.addHandler(stream_handler)
    return my_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''
    returns a connector to the database
    (mysql.connector.connection.MySQLConnection object)
    '''
    user = os.getenv("PERSONAL_DATA_DB_USERNAME")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    host = os.getenv("PERSONAL_DATA_DB_HOST")
    db = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(user=user, password=password,
                                   host=host, database=db)


def main():
    '''
    database connection using get_db and retrieve all rows in the
    users table and display each row
    '''
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    log = get_logger()
    for row in cursor:
        log.info(
            f"name={row[0]}; email={row[1]}; phone={row[2]}; \
ssn={row[3]}; password={row[4]}; ip={row[5]}; \
last_login={row[6]}; user_agent={row[7]}")


if __name__ == "__main__":
    main()
