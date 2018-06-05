import MySQLdb as mdb

host = "localhost"
user = "bookuser"
pwd = "book"
db = "bookdb"


'''
Add a book given a name, author and price.
Tags are given as a list and inserted into Tags table
one by one
'''
def addBook(name, author, price, tags):
    query = """INSERT INTO Books(book_name, author, price) \
               VALUES(%s, %s, %s)"""

    conn = mdb.connect(host, user, pwd, db)
    with conn:
        cur = conn.cursor()
        cur.execute(query, (name, author, price))

        rowid = cur.lastrowid
        for t in tags:
            tagquery = """INSERT INTO Tags(b_id, tag_name) \
                          VALUES(%s, %s)"""
            cur.execute(tagquery, (rowid, t))        
        

'''
Get all Books and concatenate their tag information together
By default GROUP_CONCAT will skip over books that do not have tags.
This implementation does not skip over these books and displays their tags as empty strings
'''
def getAllBooks():
    query = """SELECT b.book_name, b.author, b.price, \
               IFNULL(GROUP_CONCAT(t.tag_name order by t.tag_name asc separator ', '), '') as Tags \
               FROM Books b \
               LEFT JOIN Tags t \
               ON t.b_id = b.book_id \
               GROUP BY t.b_id, b.book_name, b.author, b.price\
               ORDER BY b.author"""

    conn = mdb.connect(host, user, pwd, db)
    with conn:
        cur = conn.cursor()
        cur.execute(query)
        
        rows = cur.fetchall()
        for row in rows:
            print(row)

    return rows


'''
Delete a book given by a book name and book author
'''
def delBook(b_name, b_author):
    query = """DELETE FROM Books \
               WHERE book_name = %s AND author = %s"""
    conn = mdb.connect(host, user, pwd, db)
    with conn:
        cur = conn.cursor()
        cur.execute(query, (b_name, b_author))


'''
Delete a book given an ID. Included for completeness.
'''
def delBookByID(bookID):
    query = """DELETE FROM Books \
               WHERE book_id = %s"""
    conn = mdb.connect(host, user, pwd, db)
    with conn:
        cur = conn.cursor()
        cur.execute(query, (bookID,))


'''
Rename tagname to newtag for the book with name and author.
'''
def renameTag(tagname, newtag, b_name, b_author):
    query = """UPDATE Tags t \
                LEFT JOIN Books b ON b.book_id = t.b_id \
                SET t.tag_name = %s \
                WHERE b.book_name = %s AND b.author = %s \
                AND t.tag_name = %s"""
    
    conn = mdb.connect(host, user, pwd, db)
    with conn:
        cur = conn.cursor()
        cur.execute(query, (newtag, b_name, b_author, tagname))


'''
Rename tag by its ID. Included for completeness.
'''
def renameTagByID(newtag, tagID):
    query = """UPDATE Tags t \
               SET tag_name = %s \
               WHERE tag_id = %s"""

    conn = mdb.connect(host, user, pwd, db)
    with conn:
        cur = conn.cursor()
        cur.execute(query, (newtag, tagID))


'''
Filter for Books using various parameters.
Filters through a table equivalent to the output of getallbooks.
Filtering tags selects a substring of a list of tags (i.e. 'tagA, tabB')
'''
def filterBook(limit=10, tag=None, b_name="", b_author="", price=None):
    arglst = []
    queryval = ""

    if tag:
        arglst.append("""t2.Tags LIKE '%{}%'""".format(tag))
    if b_name:
        arglst.append("""t2.book_name LIKE '%{}%'""".format(b_name))
    if b_author:
        arglst.append("""t2.author LIKE '%{}%'""".format(b_author))
    if price:
        arglst.append("t2.price <= {}""".format(price))

    if len(arglst) > 0:
        queryval = "WHERE " + " AND ".join(arglst)

    query = """SELECT * from \
             ( \
                SELECT b.book_name, b.author, b.price, \
                IFNULL(GROUP_CONCAT(t.tag_name order by t.tag_name asc separator ', '), '') as Tags \
                FROM Books b \
                LEFT JOIN Tags t \
                ON t.b_id = b.book_id \
                GROUP BY t.b_id, b.book_name, b.author, b.price \
                ORDER BY b.author \
             ) t2 \
             {} \
             LIMIT {}""".format(queryval, limit)

    conn = mdb.connect(host, user, pwd, db)
    with conn:
        cur = conn.cursor()
        cur.execute(query)

        rows = cur.fetchall()
        return rows