# TaskFlow

Aplicação web para gerenciamento de tarefas, desenvolvida com **Python, Flask e SQLite**.

O TaskFlow reúne tarefas em um painel simples, com categorias, prioridades e acompanhamento de status. Este projeto faz parte do meu portfólio de desenvolvimento.

## Funcionalidades

- Cadastro e gerenciamento de tarefas
- Organização por categorias
- Definição de prioridades
- Acompanhamento de tarefas pendentes, em andamento e concluídas
- Painel com resumo das tarefas
- Interface responsiva com tema visual

## Tecnologias

- Python
- Flask
- SQLite
- HTML, CSS e JavaScript

## Como executar localmente

### 1. Pré-requisitos

- Python 3.10 ou superior
- `pip`

### 2. Clone o repositório

```bash
git clone https://github.com/wevertonrichard75-maker/TaskFlow.git
cd TaskFlow/TaskFlow
```

### 3. Crie e ative um ambiente virtual

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Inicie a aplicação

```bash
python app.py
```

Abra no navegador o endereço local indicado pelo Flask, normalmente http://127.0.0.1:5000.

## Estrutura do projeto

```text
TaskFlow/
├── app.py
├── database.py
├── requirements.txt
├── templates/
├── static/
└── database/
```

## Próximas melhorias

- Autenticação e contas de usuário
- Testes automatizados
- Proteção CSRF e operações de alteração via POST
- Configuração segura para produção
- Implantação online para demonstração

## Observação

Este projeto está em desenvolvimento e deve ser executado localmente para avaliação. Antes de utilizá-lo em produção ou armazenar dados reais, implemente e valide os controles de segurança necessários.

## Autor

**Weverton Richard Souza Melo**

- GitHub: [@wevertonrichard75-maker](https://github.com/wevertonrichard75-maker)
