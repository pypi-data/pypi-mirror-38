# -*- coding: utf-8 -*-
import datetime

from pyzure.connection import connect
from pyzure.create import existing_test
from pyzure.execute import execute_query
from . import create
import concurrent.futures


class C:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def send_to_azure_from_one_thread(x):
    d = datetime.datetime.now()
    send_to_azure(x["instance"], x["data"], x["thread_number"])
    return (datetime.datetime.now() - d).seconds


def create_a_batch(rows, batch_size, i):
    return rows[batch_size * i:batch_size * (i + 1)]


def send_to_azure_multi_threads(instance, data, nb_threads=4, replace=True, types=None, primary_key=()):
    # Time initialization
    start = datetime.datetime.now()

    # Extract info
    table_name = data["table_name"]
    columns_name = data["columns_name"]
    rows = data["rows"]
    total_len_data = len(data["rows"])

    # Create table if needed
    if not existing_test(instance, table_name) or (types is not None) or (primary_key != ()):
        create.create_table(instance, data, primary_key, types)

    # Clean table if needed
    if replace:
        cleaning_function(instance, table_name)

    # Define batch size
    batch_size = int(total_len_data / nb_threads) + 1
    if total_len_data < nb_threads:
        batch_size = 1

    # Split data in batches of batch_size length
    split_data = []
    for i in range(nb_threads):
        split_data.append(
            {
                "data":
                    {
                        "table_name": table_name,
                        "columns_name": columns_name,
                        "rows": create_a_batch(rows, batch_size, i)
                    },
                "instance": instance,
                "thread_number": i
            }
        )

    with concurrent.futures.ProcessPoolExecutor() as executor:
        r = list(executor.map(send_to_azure_from_one_thread, split_data))

    total_length_data = 0
    for element in split_data:
        total_length_data = total_length_data + len(element["data"]["rows"])

    for i in range(len(r)):
        print("Thread %s : %s seconds" % (str(i), str(r[i])))

    print("Total rows: %s" % str(total_length_data))
    print(C.BOLD + "Total time in seconds : %s" % str((datetime.datetime.now() - start).seconds) + C.ENDC)
    return 0


def cleaning_function(instance, table_name):
    cleaning_request = '''DELETE FROM ''' + table_name + ''';'''
    print(C.WARNING + "Cleaning" + C.ENDC)
    execute_query(instance, cleaning_request)
    print(C.OKBLUE + "Cleaning Done" + C.ENDC)


def send_to_azure(instance, data, thread_number):
    """
    data = {
        "table_name" 	: 'name_of_the_azure_schema' + '.' + 'name_of_the_azure_table' #Must already exist,
        "columns_name" 	: [first_column_name,second_column_name,...,last_column_name],
        "rows"		: [[first_raw_value,second_raw_value,...,last_raw_value],...]
    }
    """
    cnxn = connect(instance)
    cursor = cnxn.cursor()
    rows = data["rows"]
    if not rows:
        return 0
    columns_name = data["columns_name"]
    table_name = data["table_name"]

    small_batch_size = int(2099 / len(columns_name))

    # Initialize counters
    boolean = True
    total_rows = len(rows)
    question_mark_pattern = "(%s)" % ",".join(["?" for i in range(len(rows[0]))])
    counter = 0
    while boolean:
        temp_row = []
        question_mark_list = []
        for i in range(small_batch_size):
            if rows:
                temp_row.append(rows.pop())
                question_mark_list.append(question_mark_pattern)
            else:
                boolean = False
                continue
        counter = counter + len(temp_row)
        percent = round(float(counter*100) / total_rows)
        print("Thread %s : %s %% rows prepared to be sent" % (str(thread_number), str(percent)))
        data_values_str = ','.join(question_mark_list)
        columns_name_str = ", ".join(columns_name)
        inserting_request = '''INSERT INTO %s (%s) VALUES %s ;''' % (table_name, columns_name_str, data_values_str)

        final_data = [y for x in temp_row for y in x]
        if final_data:
            cursor.execute(inserting_request, final_data)

    cnxn.commit()
    print(C.OKGREEN + "Committed" + C.ENDC)
    cursor.close()
    cnxn.close()
    return 0


def test():
    data = {
        "table_name": 'testaz.test2',
        "columns_name": ["nom", "prenom", "age", "date"],
        "rows": [["pif", "pif", 12, "2017-02-23"] for v in range(2000000)]
    }
    send_to_azure_multi_threads(
        "MH_TEST",
        data,
        replace=False,
        nb_threads=4
    )
