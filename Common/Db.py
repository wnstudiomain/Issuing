# import yaml
# import psycopg2
#
# with open("/home/nhanis/python/tests/nl4.yaml", "r") as ymlfile:
#     cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
#
#
# def db_connect(name):
#     connect = psycopg2.connect(
#         user=cfg["connectors"][name]["user"],
#         password=cfg["connectors"][name]["password"],
#         host=cfg["connectors"][name]["host"],
#         port="5432",
#         database=cfg["connectors"][name]["dbname"]
#     )
#     return connect
#     # Курсор для выполнения операций с базой данных