# Importa a classe da aplicação, o renderizador HTML, os dados enviados pelos
# formulários e as funções usadas para redirecionar o navegador.
from flask import Flask, render_template, request, redirect, url_for
# Importa o SQLite, banco de dados local que armazena as tarefas em um arquivo.
import sqlite3
# Importa Path para montar caminhos que funcionam em qualquer pasta de execução.
from pathlib import Path

# Cria o objeto principal que recebe as rotas e inicia o servidor web.
app = Flask(__name__)

# Usa a pasta do próprio app.py como referência. Assim, o banco é encontrado
# mesmo quando o programa é executado a partir da raiz do projeto.
DATABASE = Path(__file__).parent / "database" / "tasks.db"


def get_db_connection():
    # Abre uma conexão com o arquivo SQLite.
    conn = sqlite3.connect(DATABASE)
    # Faz cada resultado se comportar como um dicionário, permitindo usar
    # task["title"] no template em vez de depender da posição da coluna.
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # Garante que a pasta database exista antes de criar o arquivo SQLite.
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    conn = get_db_connection()
    # Cria a tabela na primeira execução. IF NOT EXISTS evita apagar dados
    # ou gerar erro quando a tabela já foi criada anteriormente.
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0,
            category TEXT DEFAULT 'Outros',
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'Média'
        )
        """
    )
    # Lê as colunas atuais para permitir atualizar bancos antigos sem recriá-los.
    columns = {row[1] for row in conn.execute("PRAGMA table_info(tasks)")}
    if "category" not in columns:
        # Adiciona categoria em instalações que foram criadas antes desse recurso.
        try:
            conn.execute("ALTER TABLE tasks ADD COLUMN category TEXT DEFAULT 'Outros'")
        except sqlite3.OperationalError as error:
            if "duplicate column name" not in str(error):
                raise
    if "status" not in columns:
        # Adiciona status em instalações antigas e converte tarefas concluídas.
        try:
            conn.execute("ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT 'pending'")
        except sqlite3.OperationalError as error:
            if "duplicate column name" not in str(error):
                raise
        conn.execute("UPDATE tasks SET status = 'completed' WHERE completed = 1")
    if "priority" not in columns:
        # Adiciona a prioridade padrão às tarefas criadas na versão anterior.
        try:
            conn.execute("ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'Média'")
        except sqlite3.OperationalError as error:
            if "duplicate column name" not in str(error):
                raise
    # Confirma todas as alterações e fecha o arquivo para liberar o recurso.
    conn.commit()
    conn.close()


@app.route("/")
def index():
    # Abre o banco apenas durante a consulta da página inicial.
    conn = get_db_connection()
    # Ordena pelo ID decrescente para mostrar as tarefas novas primeiro.
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    conn.close()
    # Calcula os indicadores do dashboard a partir dos dados reais das tarefas.
    total = len(tasks)
    completed = sum(task["status"] == "completed" for task in tasks)
    in_progress = sum(task["status"] == "in_progress" for task in tasks)
    pending = total - completed - in_progress
    categories = {category: sum(task["category"] == category for task in tasks) for category in {task["category"] for task in tasks}}
    # Entrega a lista ao Jinja, que transforma index.html em HTML no navegador.
    return render_template("index.html", tasks=tasks, total=total, completed=completed, in_progress=in_progress, pending=pending, categories=categories)


@app.route("/add", methods=["POST"])
def add_task():
    # request.form contém os campos enviados pelo formulário via método POST.
    title = request.form["title"]
    description = request.form.get("description", "")
    category = request.form.get("category", "Outros")
    priority = request.form.get("priority", "Média")
    conn = get_db_connection()
    conn.execute(
        # Os sinais ? separam o SQL dos valores e evitam problemas de injeção.
        # Toda tarefa nova começa pendente até o usuário iniciar seu trabalho.
        "INSERT INTO tasks (title, description, category, priority, status) VALUES (?, ?, ?, ?, 'pending')",
        (title, description, category, priority),
    )
    conn.commit()
    conn.close()
    # Redireciona em vez de renderizar diretamente para atualizar a lista
    # e impedir o reenvio do formulário ao recarregar a página.
    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    # Recebe o ID convertido para inteiro pela rota e atualiza apenas essa tarefa.
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET completed = 1, status = 'completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    # Volta ao dashboard para exibir o novo status imediatamente.
    return redirect(url_for("index"))


@app.route("/start/<int:task_id>")
def start_task(task_id):
    # Move uma tarefa pendente para em andamento sem marcar completed como 1.
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET status = 'in_progress' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    # Exclui somente o registro cujo ID foi informado no link da tarefa.
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    # Atualiza a lista sem a tarefa removida.
    return redirect(url_for("index"))


if __name__ == "__main__":
    # Este bloco só roda ao executar app.py diretamente, e não ao importá-lo.
    # Primeiro prepara a estrutura do banco e depois inicia o servidor local.
    init_db()
    app.run(debug=True)
