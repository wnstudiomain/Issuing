import pytest
from Common.Db import db_connect_back
from psycopg2 import Error

#from conftest import db_connect


class Dbquery:

    @staticmethod
    def get_max_de011():
        connection = db_connect_back()
        try:
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

        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Соединение с PostgreSQL закрыто")
