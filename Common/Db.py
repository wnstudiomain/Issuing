from os import environ as env
import yaml
import psycopg2

with open("/home/nhanis/python/tests/nl4.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


def db_connect_back():
    connect = psycopg2.connect(
        user=env.get('DB_BACK_USER'),
        password=env.get('DB_BACK_PASSWORD'),
        host=env.get('DB_BACK_HOST'),
        port="5432",
        database=env.get('DB_BACK_NAME')
    )
    return connect
    # Курсор для выполнения операций с базой данных