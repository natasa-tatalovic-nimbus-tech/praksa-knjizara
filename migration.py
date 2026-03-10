# import csv, date, os, psycopg2
import csv
from datetime import date
import os
import psycopg2 # open source database adapter for Python 

def main():

    print(" --- Migrations start --- ")

    # Connecting to existing data base # Connection for Python and PostgreSQL server
    # seed.py has already created the knjizaraa database
    conn = psycopg2.connect(
     dbname = "knjizara", 
     user = os.environ.get("USER"), 
     password = "", 
     host = "localhost",
     port = "5432"
)
    conn.autocommit = True
    cur = conn.cursor()


    # List to store data
    godine = []
    knjige = []

    with open('knjige.csv', mode='r') as file: 
        csvFile = csv.DictReader(file)
        # print(csvFile) - this is a csv DictReader object
        for lines in csvFile: 
            knjige.append(lines)
            godine.append(lines['godina'])
            # print("Lines and years")
            # print(lines)
            # return whole line as dictionary value
            # {'autor_id': '1', 'naslov': 'Prokleta avlija', 'cena': '900.00', 'godina': '1954'}
            # print(lines['godina']) # returns a year
            
    # print(knjige) # everything written down 
    # starost_knjiga = count_book(godine)
    # print(starost_knjiga)

    for knjiga in knjige: # rows from CSV list : knjige
        cur.execute("INSERT INTO knjige (autor_id, naslov, cena, godina) VALUES (%s, %s, %s, %s)", (knjiga['autor_id'], knjiga['naslov'], knjiga['cena'], knjiga['godina']))
        print("Data is insert to database")
        
    # select all booksk from database    
    cur.execute("SELECT id, godina FROM knjige ")
    print("--- Selected all ---")
    svi_redovi = cur.fetchall() # in list svi_redovi we have id and goidna
    print(svi_redovi)
    
    godine_baza = [red[1] for red in svi_redovi] # list comprehention 
    godine = count_book(godine_baza)
    print(godine)


    for i, red in enumerate(svi_redovi): 
        id = red[0]
        starost=godine[i]
        cur.execute("UPDATE knjige SET starost_knjige = %s WHERE id = %s", (starost, id))

    # prolaz 1
    # i = 0
    # red 1,1945
    # id = 1
    # starost = godine[0] - prva izraacunata godina
    
    # ovo na kraju skripte        
    cur.close()
    conn.close()


def count_book(godine):
    current_date = date.today()
    current_year = current_date.year
    # print(current_year)

    book_age = []
    for g in godine:
        count = current_year-int(g)
        book_age.append(count)
        # print(book_age)

    return book_age


if __name__== "__main__":
    main()