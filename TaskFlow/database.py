# Importa o driver padrão do Python para criar e consultar um banco SQLite.
import sqlite3

# Define onde o arquivo do banco será salvo quando este script for executado.
DB_PATH = "database/tasks.db"


def init_db():
    # Abre o arquivo do banco e cria a tabela caso seja a primeira execução.
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0
        )
        """
    )
    # Confirma a criação e fecha a conexão para liberar o arquivo corretamente.
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Permite preparar o banco sem iniciar o servidor Flask.
    init_db()
    # Informa no terminal que a inicialização terminou.
    print("Database initialized.")
