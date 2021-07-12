import pytest
from psycopg2.extras import execute_values

from Common.Db import db_connect_back
from psycopg2 import Error


# from conftest import db_connect


class Dbquery:

    @staticmethod
    def get_max_de011():
        connection = db_connect_back()

        with connection:
            cursor = connection.cursor()
            query = '''SELECT 
                    firstname
                    ,lastname
                    ,othernames  as middleName
                    ,contactcode
                    ,dob as dateOfBirthday
                    ,passport as passportId
                    ,nationality
                    ,status
                    FROM cmssys.indiv 
                    where keydate = '2021-04-15' 
                    and intindivcode = '708' 
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query)
            record = cursor.fetchall()[0]
            return record

    @staticmethod
    def remove_role(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''DELETE FROM host_admin_panel.users_roles h
                       WHERE h.user_id = %s AND h.role_id = %s
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            print(f'Removed role {data[1]}')

    @staticmethod
    def remove_all_role_without(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''DELETE FROM host_admin_panel.users_roles h
                       WHERE h.user_id = %s AND h.role_id != %s
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)

    @staticmethod
    def get_all_roles():
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = ''' SELECT h.id FROM host_admin_panel.roles h
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query)
            record = cursor.fetchall()
            return record

    @staticmethod
    def add_role(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = 'INSERT INTO host_admin_panel.users_roles (user_id, role_id) VALUES (%s, %s)'
            # Выполнение SQL-запроса
            cursor.execute(query, data)

    @staticmethod
    def add_role_multi(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = 'INSERT INTO host_admin_panel.users_roles (user_id, role_id) VALUES %s'
            # Выполнение SQL-запроса
            execute_values(cursor, query, data)

    @staticmethod
    def get_user_id(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''SELECT h.id FROM host_admin_panel.users h
                       WHERE h.name = %s
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchall()[0]
            return record

    @staticmethod
    def get_role_id(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''SELECT h.id FROM host_admin_panel.roles h
                       WHERE h.name = %s
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchall()[0]
            return record

    @staticmethod
    def get_cardcode_by_app_id(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''SELECT 
                    intcardcode,
                    datecardcode
                    FROM cft.in_cards where appid = %s
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchall()[0]
            return record
