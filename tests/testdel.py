import unittest
import bookapi.api as api
import MySQLdb as mdb

host = "localhost"
user = "bookuser"
pwd = "book"
db = "bookdb"

class testdel(unittest.TestCase):

    def setUp(self):
        query = "create table Books \
                 ( \
                    book_id int unsigned auto_increment, \
                    book_name char(128), \
                    author char(100) not null, \
                    price decimal(9,2) not null, \
                    primary key (book_id), \
                    constraint name_author unique(book_name, author) \
                ) engine=InnoDB"
        queryB = "create table Tags \
                  ( \
                    tag_id int unsigned auto_increment, \
                    tag_name char(26) not null, \
                    b_id int unsigned, \
                    constraint name_tag unique(tag_name, b_id), \
                    primary key (tag_id), \
                    foreign key (b_id) references Books(book_id) \
                    on delete cascade \
                ) engine=InnoDB"
        conn = mdb.connect("localhost", "bookuser", "book", "bookdb")
        with conn:
            cur = conn.cursor()
            cur.execute("DROP TABLE IF EXISTS Tags")
            cur.execute("DROP TABLE IF EXISTS Books")
            cur.execute(query)
            cur.execute(queryB)

            data = [
                ("harry potter and the chamber of secrets", "jkrowling", 15),
                ("the name of the wind", "patrickrothfuss", 20)
            ]
            insertquery = "INSERT INTO Books(book_name, author, price) \
                           VALUES(%s, %s, %s)"

            cur.executemany(insertquery, data)


    def testdelBook(self):
        api.delBook("the name of the wind", "patrickrothfuss")
        conn = mdb.connect(host, user, pwd, db)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) from Books")

            row = cur.fetchone()
            self.assertEqual(row[0], 1)


if __name__ == '__main__':
    unittest.main()