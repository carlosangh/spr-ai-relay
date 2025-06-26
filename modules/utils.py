from rich.console import Console
import os
from dotenv import load_dotenv

console = Console()

def load_env():
    if not os.path.exists('.env'):
        console.print("[bold red]Arquivo .env não encontrado. Criando...[/bold red]")
        with open('.env', 'w') as f:
            f.write("OPENAI_API_KEY=\n")
            f.write("ANTHROPIC_API_KEY=\n")
        console.print("[bold green]Preencha as chaves no arquivo .env[/bold green]")
        exit()
    load_dotenv()

def log_response(model, prompt, response):
    os.makedirs('logs', exist_ok=True)
    with open(f'logs/{model}_log.txt', 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"PROMPT:\n{prompt}\n")
        f.write(f"RESPONSE:\n{response}\n")
        f.write(f"{'='*60}\n")
