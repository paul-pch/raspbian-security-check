import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

def configure_network_security(console: Console):
    """
    Configure la sécurité du réseau :
    - Désactive les services réseau non nécessaires.
    - Configure SSH pour utiliser des clés publiques/privées.
    - Désactive l'accès root via SSH.
    """
    console.print(Panel(Text("Configuration de la sécurité du réseau...", style="bold cyan")))


    # Désactiver les services réseau non nécessaires
    try:
        console.print(Text("Désactivation des services réseau non nécessaires...", style="bold magenta"))
        services_to_disable = ["ftp", "rpcbind", "nfs-common"]
        for service in services_to_disable:
            subprocess.run(["sudo", "systemctl", "disable", service], check=True)
            subprocess.run(["sudo", "systemctl", "stop", service], check=True)
        console.print(Text("Services réseau non nécessaires désactivés.", style="green"))
    except subprocess.CalledProcessError as e:
        console.print(Text(f"Erreur lors de la désactivation des services réseau non nécessaires: {e}", style="red"))
        return

    # Configurer SSH pour utiliser des clés publiques/privées
    try:
        console.print(Text("Configuration de SSH pour utiliser des clés publiques/privées...", style="bold magenta"))
        sshd_config_file = "/etc/ssh/sshd_config"
        sshd_config_backup = "/etc/ssh/sshd_config.bak"
        subprocess.run(["sudo", "cp", sshd_config_file, sshd_config_backup], check=True)
        with open(sshd_config_file, "a", encoding="utf-8") as file:
            file.write("\nPasswordAuthentication no\n")
            file.write("PermitRootLogin no\n")
        subprocess.run(["sudo", "systemctl", "restart", "ssh"], check=True)
        console.print(Text("SSH configuré pour utiliser des clés publiques/privées.", style="green"))
    except (subprocess.CalledProcessError, FileNotFoundError, PermissionError) as e:
        console.print(Text(f"Erreur lors de la configuration de SSH: {e}", style="red"))
        return

    console.print(Panel(Text("Configuration de la sécurité du réseau terminée.", style="bold green")))
