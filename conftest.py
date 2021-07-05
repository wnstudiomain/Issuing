import pytest
import yaml
import psycopg2

with open("nl4.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)


@pytest.fixture(scope="session")
def db_connect(name):
    connect = psycopg2.connect(
        user=cfg["connectors"][name]["user"],
        password=cfg["connectors"][name]["password"],
        host=cfg["connectors"][name]["host"],
        port="5432",
        database=cfg["connectors"][name]["dbname"]
    )
    return connect
