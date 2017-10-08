import sqlite3

connection = sqlite3.connect("test.db")
cursor = connection.cursor()
cursor.execute("drop table if exists test_tbl")
cursor.execute("create table test_tbl (id_col varchar, value_col)")


def set_value(name, value):
    cursor.execute("insert into test_tbl (id_col, value_col) values ('%s', '%s')" % (name, value))
    return


def get_value(name):
    cursor.execute("select value_col from test_tbl where id_col='%s'" % name)
    return cursor.fetchone()


def test():
    set_value('grzmelik', 'wahmurka')
    print (get_value("grzmelik"))
    assert ('wahmurka' == get_value('grzmelik')[0])

test()
