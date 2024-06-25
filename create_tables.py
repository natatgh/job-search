import sqlite3

def create_tables():
    # Conectar ao banco de dados (ou criar se não existir)
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()

    # Criar a tabela jobs se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            company TEXT,
            location TEXT,
            link TEXT
        )
    ''')

    # Verificar se a coluna description existe e adicioná-la se não existir
    cursor.execute("PRAGMA table_info(jobs)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'description' not in columns:
        cursor.execute('ALTER TABLE jobs ADD COLUMN description TEXT')

    # Salvar as mudanças e fechar a conexão
    conn.commit()
    conn.close()

def main():
    create_tables()

    # Restante do código aqui...

if __name__ == "__main__":
    main()
