import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

def configure_users(console: Console):
    """
    Configure les utilisateurs selon les spécifications :
    - Supprime les utilisateurs "raspberry" et "pi" s'ils existent.
    - Désactive la connexion par mot de passe pour l'utilisateur "root".
    """
    console.print(Panel(Text("Configuration des utilisateurs...", style="bold cyan")))

    # Supprimer les utilisateurs "raspberry" et "pi" s'ils existent
    users_to_remove = ["raspberry", "pi"]
    for user in users_to_remove:
        try:
            subprocess.run(["id", user], check=True)
            console.print(Text(f"L'utilisateur '{user}' existe. Suppression de l'utilisateur '{user}'...", style="yellow"))
            try:
                subprocess.run(["sudo", "userdel", "-r", user], check=True)
                console.print(Text(f"L'utilisateur '{user}' a été supprimé.", style="green"))
            except subprocess.CalledProcessError as e:
                console.print(Text(f"Erreur lors de la suppression de l'utilisateur '{user}': {e}", style="red"))
        except subprocess.CalledProcessError:
            console.print(Text(f"L'utilisateur '{user}' n'existe pas.", style="green"))

    # Désactiver la connexion par mot de passe pour l'utilisateur "root"
    try:
        subprocess.run(["sudo", "passwd", "-l", "root"], check=True)
        console.print(Text("La connexion par mot de passe pour l'utilisateur 'root' a été désactivée.", style="green"))
    except subprocess.CalledProcessError as e:
        console.print(Text(f"Erreur lors de la désactivation de la connexion par mot de passe pour l'utilisateur 'root': {e}", style="red"))

    console.print(Panel(Text("Configuration des utilisateurs terminée.", style="bold green")))
