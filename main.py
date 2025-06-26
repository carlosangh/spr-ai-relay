from modules.openai_relay import ask_openai
from modules.claude_relay import ask_claude
from modules.utils import load_env, log_response
from rich.console import Console

console = Console()

def main():
    load_env()

    console.print("[bold cyan]=== SPR AI RELAY INTELIGENTE ===[/bold cyan]")
    console.print("[bold yellow]Use: 'gpt' ou 'claude' + sua pergunta. Digite 'exit' para sair.[/bold yellow]\n")

    while True:
        prompt = input("> ")

        if prompt.lower() == "exit":
            console.print("[bold red]Encerrando...[/bold red]")
            break

        if prompt.lower().startswith("gpt"):
            clean_prompt = prompt[3:].strip()
            response = ask_openai(clean_prompt)
            console.print(f"\n[bold blue]OpenAI respondeu:[/bold blue]\n{response}")
            log_response("openai", clean_prompt, response)
            continue

        if prompt.lower().startswith("claude"):
            clean_prompt = prompt[6:].strip()
            response = ask_claude(clean_prompt)
            console.print(f"\n[bold yellow]Claude respondeu:[/bold yellow]\n{response}")
            log_response("claude", clean_prompt, response)
            continue

        console.print("[bold red]⚠️ Especifique o modelo: 'gpt' ou 'claude' no início do prompt.[/bold red]")


if __name__ == "__main__":
    main()
