import sqlite3

def list_tables(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tabelas no banco de dados:")
    for table in tables:
        print(table[0])

    conn.close()

def list_table_content(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"Colunas na tabela '{table_name}':")
    for column in columns:
        print(column[1])

    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    print(f"Dados na tabela '{table_name}':")
    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    db_name = 'jobs.db'
    table_name = 'jobs'
    
    list_tables(db_name)
    list_table_content(db_name, table_name)
