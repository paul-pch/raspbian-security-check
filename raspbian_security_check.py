from rich.console import Console
from rich.panel import Panel
from rich.text import Text

import steps.security as security

def main():
    console = Console()

    # Créer un message d'initialisation
    message = Text("Initialisation du script de sécurité pour Raspberry Pi", style="bold magenta")

    # Afficher le message dans un panneau
    console.print(Panel(message, title="[bold green]Début du script", title_align="left"))


    security.update_security(console)

if __name__ == "__main__":
    main()