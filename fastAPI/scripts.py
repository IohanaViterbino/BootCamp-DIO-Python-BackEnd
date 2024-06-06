import os
import sys
import subprocess

def create_migrations():
    if len(sys.argv) < 2:
        print("Você precisa fornecer uma descrição para a migração.")
        sys.exit(1)

    description = sys.argv[1]
    os.environ["PYTHONPATH"] = f"{os.environ.get('PYTHONPATH', '')}:{os.getcwd()}"
    try:
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", description], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar migração: {e}")
        sys.exit(1)

def run_migrations():
    os.environ["PYTHONPATH"] = f"{os.environ.get('PYTHONPATH', '')}:{os.getcwd()}"
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao rodar migrações: {e}")
        sys.exit(1)
