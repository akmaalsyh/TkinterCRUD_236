import sqlite3
con = sqlite3.connect("tutorial.db")
cur = con.cursor()
_title=input("Masukkan judul Movie: ")
_year=input("Masukkan tahun release: ")
_rating=input("Masukkan rating movienya ")
#cur.execute("""CREATE TABLE movie
 #   (title text, year int, score double)""")
cur.execute("""
    INSERT INTO movie VALUES
        ('{}', {}, {})
""".format(_title,_year,_rating))
con.commit()