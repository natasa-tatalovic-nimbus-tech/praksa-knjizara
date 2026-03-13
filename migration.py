# This is ETL script that is used to read transform and write data to databse.
# Dockerfile should start this ETL script that I have
# Docker compose file should start postgres database and after it all scripts - creating database, shemaa and tables

# import csv, date, os, psycopg2
import csv
import os
from datetime import date

import psycopg2  # open source database adapter for Python

def run_migrations(cursor):
    
    migrations = [f for f in os.listdir('sql_migrations/') if f.endswith('.sql')]
    # migrations = migrations.sort() # nema dodele rezultata
    migrations.sort()
    print(migrations)

    for file in migrations:
        print("izvrsavanje migacije")
        with open (os.path.join('sql_migrations', file), 'r') as f: 
            sql=f.read()    # read fie
        cursor.execute(sql) # execute sql order
        print("zavrsena migracija")


def main():

    print(" --- Migrations start --- ")

    # Connecting to existing data base # Connection for Python and PostgreSQL server
    # seed.py has already created the knjizaraa database
    conn = psycopg2.connect(
     dbname = "knjizara", 
     user = os.environ.get("DB_USER"), 
     password=os.environ.get("DB_PASSWORD"), # Cha
     host=os.environ.get("DB_HOST"),    # Change1
     port = os.environ.get("DB_PORT")
)
    conn.autocommit = True
    cur = conn.cursor()


    # List to store data
    godine = []
    knjige = []

    # migration script call
    run_migrations(cur)

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
        print("Data is inserted to database")
        
    # select all booksk from database    
    cur.execute("SELECT id, godina FROM knjige ")
    print("--- Selected all ---")
    svi_redovi = cur.fetchall() # in list svi_redovi we have id and goidna
    print(svi_redovi)
    
    godine_baza = [red[1] for red in svi_redovi] # list comprehention 
    godine = count_book(godine_baza)
    print(godine)


    for i, red in enumerate(svi_redovi): 
        # id is inbuilt function in python
        idd = red[0]
        starost=godine[i]
        cur.execute("UPDATE knjige SET starost_knjige = %s WHERE id = %s", (starost, idd))

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