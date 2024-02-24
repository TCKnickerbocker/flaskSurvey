from contextlib import contextmanager
import logging
import os

from flask import current_app, g

import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import DictCursor

pool = None

def setup():
    global pool
    # current_app.logger.info(f"creating db connection pool")
    pool = ThreadedConnectionPool(1, 100, 
            dbname=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PW'),
            host=os.environ.get('DB_HOSTNAME'),
            port=os.environ.get('DB_PORT'),
            sslmode='require')


@contextmanager
def get_db_connection():
    print("Getting db con")
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    print("Getting cursor")
    with get_db_connection() as connection:
      cursor = connection.cursor(cursor_factory=DictCursor)
      # cursor = connection.cursor()
      try:
          yield cursor
          if commit:
              connection.commit()
      finally:
          cursor.close()

# Insert survey into db
def add_survey(survey_data, day):
    with get_db_cursor(True) as cur:
        cur.execute("""
            INSERT INTO surveys (what_usr_would_be, superpower, secondary_superpowers, costume_kind_value, submissionDate)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING surveyID
        """, (
            survey_data['what_usr_would_be'],
            survey_data['primary'],
            survey_data['secondary'],
            survey_data['costumeKind'],  # Will insert NULL if user never checked the box
            day,
        ))
        survey_id = cur.fetchone()[0]
        return survey_id


def get_surveys(reverse=False):
    with get_db_cursor() as cur:
        if reverse:
            cur.execute("""
                SELECT * FROM surveys
                ORDER BY surveyID
                ASC
            """)
        else:
            cur.execute("""
                SELECT * FROM surveys
                ORDER BY surveyID
                DESC
            """)
        return cur.fetchall()

def countPrimaries(reverse=False):
    with get_db_cursor() as cur:
        if reverse:
            cur.execute("""
                SELECT * FROM surveys
                ORDER BY surveyID
                ASC
            """)
        else:
            cur.execute("""
                SELECT * FROM surveys
                ORDER BY surveyID
                DESC
            """)
        return cur.fetchall()
    
def countSecondaries(reverse=False):
    with get_db_cursor() as cur:
        if reverse:
            cur.execute("""
                SELECT * FROM surveys
                ORDER BY surveyID
                ASC
            """)
        else:
            cur.execute("""
                SELECT * FROM surveys
                ORDER BY surveyID
                DESC
            """)
        return cur.fetchall()

def getCounts(key):
    with get_db_cursor() as cur:
        cur.execute("""
            SELECT %s, COUNT(*) FROM surveys
            GROUP BY %s DESC
        """,
        (key, key))
        return cur.fetchall() 



