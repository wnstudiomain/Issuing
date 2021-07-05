from Common import dbquery


def test_failing():
    record = dbquery.Dbquery.get_max_de011()
    List = ['1', '2', '008']
    print("Результат", record)
    print(type(record))
    length = len(record)
    for key in range(length):
        if record[key] in List:
            print(record[key])
            assert '008' == record[key]
