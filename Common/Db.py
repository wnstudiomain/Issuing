from os import environ as env
import yaml
import psycopg2


def db_connect_back():
    connect = psycopg2.connect(
        user=env.get('DB_BACK_USER'),
        password=env.get('DB_BACK_PASSWORD'),
        host=env.get('DB_BACK_HOST'),
        port="5432",
        database=env.get('DB_BACK_NAME')
    )
    return connect


def db_connect_aq():
    connect = psycopg2.connect(
        user=env.get('DB_AQ_USER'),
        password=env.get('DB_AQ_PASSWORD'),
        host=env.get('DB_AQ_HOST'),
        port="5432",
        database=env.get('DB_AQ_NAME')
    )
    return connect


def db_connect_front():
    connect = psycopg2.connect(
        user=env.get('DB_FRONT_USER'),
        password=env.get('DB_FRONT_PASSWORD'),
        host=env.get('DB_FRONT_HOST'),
        port="5432",
        database=env.get('DB_FRONT_NAME')
    )
    return connect

