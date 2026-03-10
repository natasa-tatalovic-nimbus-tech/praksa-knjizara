import psycopg2 # library for app that create and destroy a lot of cursors and a
import os

# # Connection to 'knjizara' database
# e = os.environ.get("USER")
# print("This is enviroronment:", e)

def run_sql(cursor, filepath):
    print(f"--- Starting --- {filepath}")
    with open(filepath, "r") as f:
        sql = f.read()

    cursor.execute(sql)
    print(f"--- Executed ---! {filepath}")

def main(): 

    print("--- Seeding ---")
    
    # Create database # 
    print("--- Creating database ---") # Connnection to postgres
    conn = psycopg2.connect(
     dbname = "postgres", 
     user = os.environ.get("USER"), 
     password = "", 
     host = "localhost",
     port = "5432"
    )

    # Autocommit #
    conn.autocommit = True
    # change the behaviour of commit
    print(f"Autocommit: {conn.autocommit}")
    cur = conn.cursor() # cursor ready for commandds
    # Command
    cur.execute("SELECT 1 FROM pg_database WHERE datname ='knjizara'") # this is an requ to postgreSQL to do the action

    if not cur.fetchone():
        # SQL function that runs the sql action to create database
        run_sql(cur, "sql_create/create_database.sql")
    else:
        print("Exsisting database")

    # We have closed connection 
    cur.close()
    conn.close()


    # We are using a new database - we create a new connection  
    # Connecting directly to database we have previously created
    print("--- Creating sheme and tables ---") # Connection to knjizara
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

    print("--- Data input ---") # the order is important becasue of fogein keys
    run_sql(cur, "sql_seed/seed_autori.sql")
    run_sql(cur, "sql_seed/seed_knjige.sql")
    run_sql(cur, "sql_seed/seed_narudzbine.sql")

    cur.close()
    conn.close()

# main function 
if __name__ == "__main__": 
    main()