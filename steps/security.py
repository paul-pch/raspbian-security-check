import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def update_security(console: Console):
    """
    Vérifie et applique les mises à jour de sécurité.
    """
    console.print(Panel(Text("Vérification des mises à jour de sécurité...", style="bold cyan")))

    # Mettre à jour la liste des paquets
    try:
        subprocess.run(["apt-get", "update"], check=True)
        console.print(Text("Liste des paquets mise à jour.", style="green"))
    except subprocess.CalledProcessError as e:
        console.print(Text(f"Erreur lors de la mise à jour de la liste des paquets: {e}", style="red"))
        return

    # Installer unattended-upgrades
    try:
        subprocess.run(["apt-get", "install", "unattended-upgrades", "-y"], check=True)
        console.print(Text("unattended-upgrades installé.", style="green"))
    except subprocess.CalledProcessError as e:
        console.print(Text(f"Erreur lors de l'installation de unattended-upgrades: {e}", style="red"))
        return

    # # Exécuter unattended-upgrade en mode dry-run # TODO à réparer => ModuleNotFoundError: No module named 'apt'
    # try:
    #     subprocess.run(["unattended-upgrade", "-d", "-v", "--dry-run"], check=True)
    #     console.print(Text("Mises à jour de sécurité vérifiées en mode dry-run.", style="green"))
    # except subprocess.CalledProcessError as e:
    #     console.print(Text(f"Erreur lors de l'exécution de unattended-upgrade en mode dry-run: {e}", style="red"))
    #     return

    # Décommenter les lignes spécifiques dans le fichier de configuration
    config_file = "/etc/apt/apt.conf.d/50unattended-upgrades"
    try:
        with open(config_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open(config_file, "w", encoding="utf-8") as file:
            for line in lines:
                if "Unattended-Upgrade::Remove-Unused-Kernel-Packages" in line:
                    line = line.replace("//", "")
                if "Unattended-Upgrade::SyslogEnable" in line:
                    line = line.replace("//", "")
                file.write(line)

        console.print(Text("Lignes spécifiques décommentées dans le fichier de configuration.", style="green"))
    except FileNotFoundError as e:
        console.print(Text(f"Erreur lors de la récupération du fichier de configuration: {e}", style="red"))
        return
    except PermissionError as e:
        console.print(Text(f"Erreur de permission lors de la récupération du fichier de configuration: {e}", style="red"))
        return

    # Reconfigurer unattended-upgrades
    try:
        subprocess.run(["dpkg-reconfigure", "--priority=medium", "--frontend=noninteractive", "unattended-upgrades"], check=True)
        console.print(Text("unattended-upgrades reconfiguré.", style="green"))
    except subprocess.CalledProcessError as e:
        console.print(Text(f"Erreur lors de la reconfiguration de unattended-upgrades: {e}", style="red"))
        return

    # Mettre à jour les paquets installés
    try:
        subprocess.run(["apt", "upgrade", "-y"], check=True)
        console.print(Text("Paquets installés mis à jour.", style="green"))
    except subprocess.CalledProcessError as e:
        console.print(Text(f"Erreur lors de la mise à jour des paquets installés: {e}", style="red"))
        return

    # Nettoyer les paquets inutilisés
    try:
        subprocess.run(["apt", "autoremove", "-y"], check=True)
        console.print(Text("Paquets inutilisés nettoyés.", style="green"))
    except subprocess.CalledProcessError as e:
        console.print(Text(f"Erreur lors du nettoyage des paquets inutilisés: {e}", style="red"))
        return

    console.print(Panel(Text("Mises à jour de sécurité terminées.", style="bold green")))
