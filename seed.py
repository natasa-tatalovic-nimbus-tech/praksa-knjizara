import psycopg2 # library for app that create and destroys a loto of cursors and a
import os

# Connection to 'knjizara' database
e = os.environ.get("USER")
print("This is enviroronment:", e)

print("Starting the connection process")
conn = psycopg2.connect(
     dbname = "postgres", 
     user = os.environ.get("USER"), 
     password = "", 
     host = "localhost",
     port = "5432"
)

def run_sql(cursor, filepath):
    print(f"Pokrrece se fajl {filepath}")
    with open(filepath, "r") as f:
        sql = f.read()

    cursor.execute(sql)
    print(f"Izvrsen {filepath}")

def main(): 
    print("Pocetakk seedinga")

    print("Kreiranje baze")
    conn = psycopg2.connect(
     dbname = "postgres", 
     user = os.environ.get("USER"), 
     password = "", 
     host = "localhost",
     port = "5432"
)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname ='knjizara'")
    if not cur.fetchone():
        run_sql(cur, "sql_create/create_database.sql")
    else:
        print("Baza postoji ")

    cur.close()
    conn.close()

    print("Kreiranje seme i tabele")
    conn = psycopg2.connect(
     dbname = "knjizara", 
     user = os.environ.get("USER"), 
     password = "", 
     host = "localhost",
     port = "5432"
)
    conn.autocommit = True
    cur = conn.cursor()

    run_sql(cur, "sql_create/create_shema.sql")
    run_sql(cur, "sql_create/create_tables.sql")

    print("Unos podataka")
    run_sql(cur, "sql_seed/seed_autori.sql")
    run_sql(cur, "sql_seed/seed_knjige.sql")
    run_sql(cur, "sql_seed/seed_narudzbine.sql")

    cur.close()
    conn.close()

if __name__ == "__main__": 
    main()