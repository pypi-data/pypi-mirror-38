import pyodbc
from pyzure.connection.connection import connect


def execute_query_from_cnxn(cnxn, query, data, cursor=None, commit=True):
    if not cursor:
        cursor = cnxn.cursor()
    cursor.execute(query, data)
    if commit:
        cnxn.commit()
        cursor.close()
        return cnxn
    else:
        return cursor


def execute_query(instance, query, data=None, commit=True, cursor=None, cnxn=None, create_schema=False):
    if not cnxn and not cursor:
        cnxn = connect(instance)
        cursor = cnxn.cursor()

    if data:
        cursor.execute(query, data)
        if commit:
            cnxn.commit()
        result = None
    elif create_schema:
        cursor.execute(query)
        cnxn.commit()
        result = None
    else:
        cursor.execute(query)
        result = []
        try:
            columns = [column[0] for column in cursor.description]
            for row in cursor.fetchall():
                dict_ = dict()
                for i in range(len(columns)):
                    dict_[columns[i]] = row[i]
                result.append(dict_)
        except pyodbc.ProgrammingError:
            pass
        except TypeError:
            cnxn.commit()
            return []
        cnxn.commit()

    if commit:
        cursor.close()
        cnxn.close()

        return result
    else:
        return result, cursor, cnxn
