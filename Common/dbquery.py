import datetime

import pytest
from psycopg2.extras import execute_values

from Common.Db import db_connect_back, db_connect_aq, db_connect_front
from psycopg2 import Error


# from conftest import db_connect


class Dbquery:

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

    @staticmethod
    def get_cardcode_by_pan(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''SELECT 
                    intcardcode,
                    keydate
                    FROM cmssys.card where cardbin ||cardbody ||cardcheck = %s
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchall()[0]
            return record

    @staticmethod
    def get_pan_by_appid(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''SELECT 
                    c.cardbin || c.cardbody || c.cardcheck as card
                    FROM cmssys.card c
                        JOIN cft.in_cards i ON c.intcardcode = i.intcardcode AND i.datecardcode = c.keydate
                    WHERE appid = %s
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchone()[0]
            return record

    @staticmethod
    def get_card_limit(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = 'SELECT * FROM cmssys.cardlimit c WHERE c.intcardcode = %s AND c.keydate = %s'
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchone()
            colnames = [desc[0] for desc in cursor.description]
            values = [val for val in record]
            new_dict = dict(zip(colnames, values))
            return new_dict

    @staticmethod
    def get_arn(data):
        connection = db_connect_aq()
        with connection:
            cursor = connection.cursor()
            query = '''SELECT v1.acquirer_reference_number FROM vi_clearing.visa_tc5_tcr_0 v1 WHERE v1.fileseqno = %s
                       AND v1.seqno = %s'''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchone()
            return record

    @staticmethod
    def get_auth_code(data):
        connection = db_connect_front()
        with connection:
            cursor = connection.cursor()
            query = "SELECT t1.de039 FROM hs.mes_vs_in t1 WHERE t1.m_type IN ('0110','0120') AND t1.de037 = %s"
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchone()
            return record[0]

    @staticmethod
    def get_max_de011():
        connection = db_connect_front()
        date_now = (str(datetime.date.today()),);
        with connection:
            cursor = connection.cursor()
            query = "SELECT MAX(de011) FROM hs.mes_mchs_in where de037<>'930109000373' and date(add_time) = %s"
            # Выполнение SQL-запроса
            cursor.execute(query, date_now)
            record = cursor.fetchone()[0]
        with connection:
            cursor = connection.cursor()
            query = "SELECT max(t.de011) FROM hs.mes_rej_to_hs t WHERE de037 <> '930109000373' and date(add_time) = %s"
            # Выполнение SQL-запроса
            cursor.execute(query, date_now)
            c = cursor.fetchone()[0]
            record1 = c if c else ''
        if record1 and record1 > record:
            return str(int(record1) + 1).zfill(6)
        else:
            return str(int(record) + 1).zfill(6) if record else '000700'

    @staticmethod
    def get_auth_data(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''
            SELECT t1.keydate,
            t1.datemercbatch,
            t6.posdata,
            c.cardbin || c.cardbody || c.cardcheck as card,
            i.appid,
            r1.accotbval,
            t1.transvalue,
            (SELECT v1.code
            FROM cmssys.valcur v1
            WHERE v1.sintcode = t1.sinttranscur)  as transcur,
            t1.billvalue,
            (SELECT v1.code
            FROM cmssys.valcur v1
            WHERE v1.sintcode = t1.sintbillcur)   as billcur,
            t1.origbillvalue,
            (SELECT v1.code
            FROM cmssys.valcur v1
            WHERE v1.sintcode = t1.origbillcur)   as origbillcur,
            t6.de43,
            t1.mcc,
            t1.rnn,
            t6.tid,
            tc1.description,
            tc1.cmscode,
            t10.mercname,
            trim(substr(t4.description, 119))           as fseqno
            FROM cmssys.trans1 t1
            INNER JOIN cmssys.card c ON t1.intcardcode = c.intcardcode and t1.datecardcode = c.keydate
            INNER JOIN cft.in_cards i ON c.intcardcode = i.intcardcode and c.keydate = i.datecardcode
            INNER JOIN cmssys.trans6 t6 ON t1.intseqno = t6.intseqno and t1.keydate = t6.keydate
            INNER JOIN cmssys.repauth r1 ON r1.txnkeydate = t1.keydate and r1.txnintcode = t1.intseqno
            INNER JOIN cmssys.valtranscode tc1 ON t1.sintttype = tc1.sintcode
            LEFT JOIN cmssys.trans10 t10 ON t1.intseqno = t10.intseqno and t1.keydate = t10.keydate
            LEFT JOIN cmssys.trans4 t4 ON t1.intseqno = t4.intseqno and t1.keydate = t4.keydate
            WHERE t1.rnn = %s
            GROUP BY t1.keydate, t1.datemercbatch, t6.posdata, card, i.appid, r1.accotbval,
                 t1.transvalue, transcur, t1.billvalue, billcur, t1.origbillvalue, origbillcur,
                 t6.de43, t1.mcc, t1.rnn, t6.tid, tc1.description, tc1.cmscode, t10.mercname, fseqno;'''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchone()
            colnames = [desc[0] for desc in cursor.description]
            values = [val for val in record]
            new_dict = dict(zip(colnames, values))
            return new_dict

    @staticmethod
    def get_accno_by_pan(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''SELECT 
                    am.accno,
                    c.intacccode,
                    c.dateacccode
                    FROM cmssys.accountmap am
                        JOIN cmssys.card c ON am.keydate = c.dateacccode AND am.intacccode = c.intacccode
                    WHERE cardbin ||cardbody ||cardcheck = %s
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchone()
            return record

    @staticmethod
    def get_data_statement(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''
            select mb.postingdate,
            tr4.tid,
            concat(tr6.authdate, ' ', tr6.authtime) as datetime,
            c.cardbin || c.cardbody || c.cardcheck  as card,
            tr1.transvalue,
            (SELECT v1.code
                FROM cmssys.valcur v1
                WHERE v1.sintcode = tr1.sinttranscur)  as transcur,
            tr10.mercname,
            right(tr6.de43, 2)                      as country,
            tr1.billvalue,
            (SELECT v1.code
                FROM cmssys.valcur v1
                WHERE v1.sintcode = tr1.sintbillcur)   as billcur,
            tr1.origbillvalue,
            tr1.billrate,
            tr1.billrule,
            vc.creditdebit
        from cmssys.trans1 tr1
                join cmssys.trans6 tr6 on tr1.intseqno = tr6.intseqno and tr1.keydate = tr6.keydate
                join cmssys.valcur cur on tr6.authcur = cur.sintcode
                join cmssys.trans4 tr4 on tr1.intseqno = tr4.intseqno and tr1.keydate = tr4.keydate
                join cmssys.trans10 tr10 on tr1.intseqno = tr10.intseqno and tr1.keydate = tr10.keydate
                join cmssys.mercbatch mb on tr1.intmercbatch = mb.intseqno and tr1.datemercbatch = mb.keydate
                join cmssys.card c on tr1.intcardcode = c.intcardcode and tr1.datecardcode = c.keydate
                join cmssys.indivacc ia on tr1.intacccode = ia.intacccode and tr1.dateacccode = ia.keydate
                join cmssys.accountmap am on am.keydate = ia.keydate and am.intacccode = ia.intacccode
                join cmssys.valtranscode vc on vc.sintcode = tr1.sintttype
        where am.accno = %s
        and mb.postingdate >= %s
        and mb.postingdate <= %s
            '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            values = [dict(zip(colnames, val)) for val in record]
            return values

    @staticmethod
    def get_person_data(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''
            select i.intindivcode,
            i.keydate,
            i.firstname,
            i.lastname,
            ia.bankname,
            a.city,
            a.zip,
            concat(a.line1, a.line2)                                                   as address,
            (select vc.name from cmssys.valcountry vc where a.countryref = vc.sintcode) as country,
            (SELECT v1.code
            FROM cmssys.valcur v1
            WHERE v1.sintcode = cс.sintcurtype)  as cur_card     
        from cmssys.accountmap am
            join cmssys.indivacc ia on am.keydate = ia.keydate and am.intacccode = ia.intacccode
            join cmssys.indiv i on i.keydate = ia.dateindivcode and i.intindivcode = ia.intindivcode
            join cmssys.addrmap adrm on adrm.dateownercode = i.keydate and adrm.intownercode = i.intindivcode
            join cmssys.addr a on a.keydate = adrm.dateaddrcode and a.intaddrcode = adrm.intaddrcode
            right outer join cmssys.card c on ia.keydate = c.dateacccode and ia.intacccode = c.intacccode
            join cmssys.cardcont cс on cс.intcontcode = c.intcontcode
        where am.accno = %s and adrm.sintinfotype = 2;
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchone()
            return record

    @staticmethod
    def get_auth_trans6(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''SELECT 
                        tr6.*
                        FROM cmssys.trans1 tr1
                            JOIN cmssys.trans6 tr6 on tr1.intseqno = tr6.intseqno and tr1.keydate = tr6.keydate
                        WHERE rnn = %s
                        '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            values = [dict(zip(colnames, val)) for val in record]
            return values

    @staticmethod
    def get_fileseqno_by_rrn(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''SELECT
                    split_part(trim(substr(t4.description, 119)), ':', 1) as fileseqno,
                    split_part(trim(substr(t4.description, 119)), ':', 2) as seqno
                    FROM cmssys.trans1 t1
                        JOIN cmssys.trans4 t4 on t1.intseqno = t4.intseqno and t1.keydate = t4.keydate
                    WHERE t1.rnn = %s
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchone()
            return record

    @staticmethod
    def get_tr_visa_aq(data):
        connection = db_connect_aq()
        with connection:
            cursor = connection.cursor()
            query = '''SELECT
                    *
                    FROM vi_clearing.visa_tc5_tcr_0 v1 WHERE v1.fileseqno = %s
                       AND v1.seqno = %s
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchone()
            colnames = [desc[0] for desc in cursor.description]
            values = [val for val in record]
            new_dict = dict(zip(colnames, values))
            return new_dict

    @staticmethod
    def get_acc_otb(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''SELECT  cmssys.get_acc_otb(%s, %s)
                    '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchone()
            return record

    @staticmethod
    def get_intacccode_by_pan(data):
        connection = db_connect_back()
        with connection:
            cursor = connection.cursor()
            query = '''SELECT 
                        c.intacccode,
                        c.dateacccode
                        FROM cmssys.card c
                        WHERE cardbin ||cardbody ||cardcheck = %s
                        '''
            # Выполнение SQL-запроса
            cursor.execute(query, data)
            record = cursor.fetchone()
            return record