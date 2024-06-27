import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
import os
import webbrowser

def lancer_script_nmap():
    script_path = r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\Script\nmap_scan.py"
    try:
        print(f"Lancement de {script_path}")
        subprocess.Popen(["python", script_path])
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution du script Nmap : {e}")

def lancer_script_keylog():
    script_path = r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\Script\keylog.py"
    try:
        print(f"Lancement de {script_path}")
        subprocess.Popen(["python", script_path])
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution du script de Keylogger : {e}")

def lancer_script_shell():
    script_path = r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\Script\shellreverse.py"
    try:
        print(f"Lancement de {script_path}")
        subprocess.Popen(["python", script_path])
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution du script Metasploit : {e}")

def lancer_script_bruteforce():
    script_path = r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\Script\bruteforce.py"
    try:
        print(f"Lancement de {script_path}")
        subprocess.Popen(["python", script_path])
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution du script BruteForce : {e}")

def lancer_script_cve():
    script_path = r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\Scriptcve\cve.py"
    try:
        print(f"Lancement de {script_path}")
        subprocess.Popen(["python", script_path])
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'exécution du script cve : {e}")

def load_scripts():
    scripts_combobox["values"] = ("Choisissez votre script", "Lancer le script Nmap", "Lancer le script de Keylogger", "Lancer le script Reverse shell", "Lancer le script de BruteForce", "Lancer le script de Détection de vulnérabilités")
    scripts_combobox.set("Choisissez votre script")

def on_script_selected(event):
    selection = scripts_combobox.get()
    print(f"Script sélectionné : {selection}")
    if selection == "Lancer le script Nmap":
        lancer_script_nmap()
    elif selection == "Lancer le script de Keylogger":
        lancer_script_keylog()
    elif selection == "Lancer le script Reverse shell":
        lancer_script_shell()
    elif selection == "Lancer le script de BruteForce":
        lancer_script_bruteforce()
    elif selection == "Lancer le script de Détection de vulnérabilités":
        lancer_script_cve()

def resize_image(event):
    global background_image, background_photo
    aspect_ratio = background_image.width / background_image.height
    new_width = max(1, event.width)
    new_height = int(new_width / aspect_ratio)
    if new_height > event.height:
        new_height = event.height
        new_width = int(new_height * aspect_ratio)
    new_width = max(1, new_width)
    new_height = max(1, new_height)
    resized_image = background_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(resized_image)
    canvas.itemconfig(canvas_image, image=background_photo)
    canvas.config(width=new_width, height=new_height)

def generer_rapport_complet():
    rapports = {
        "rapport.html": r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\result_nmap\rapport.html",
        "listkey.txt": r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\result_keylog\keylog.txt",
        "result-reverse": r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\result-reverse",
        "result-bruteforce": r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\result-bruteforce",
        "result_cve": r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\result_cve"
    }

    rapport_html = r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\rapport_complet.html"

    html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Rapport Complet</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        h2 { color: #666; }
        h3 { color: #777; }
        pre { background-color: #f4f4f4; padding: 10px; border: 1px solid #ddd; overflow-x: auto; }
        a { text-decoration: none; color: #0066cc; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>Rapport Complet</h1>
"""

    for title, path in rapports.items():
        html_content += f"<h2>{title}</h2>\n"
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                html_content += f"<pre>{content}</pre>\n"
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    html_content += f"<h3>{file_path}</h3>\n"
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                        html_content += f"<pre>{content}</pre>\n"
        else:
            html_content += f"<p>{path} (non trouvé)</p>\n"

    html_content += """
</body>
</html>
"""

    with open(rapport_html, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"Rapport HTML créé avec succès : {rapport_html}")
    return rapport_html

def generer_rapport():
    try:
        rapport_path = generer_rapport_complet()
        if messagebox.askyesno("Succès", "Rapport HTML créé avec succès. Voulez-vous l'ouvrir ?"):
            webbrowser.open('file://' + os.path.realpath(rapport_path))
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la génération du rapport HTML : {e}")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Menu Sélectionnable")
root.geometry("600x400")

# Chargement de l'image de fond
image_path = r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\images\menu.jpg"
background_image = Image.open(image_path)
background_photo = ImageTk.PhotoImage(background_image)

# Création du canvas avec l'image de fond
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)
canvas_image = canvas.create_image(0, 0, anchor=tk.NW, image=background_photo)

# Création du cadre au centre de la fenêtre
frame = tk.Frame(root, bg="white")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Création du titre "TOOL BOX"
title_label = tk.Label(frame, text="TOOL BOX", font=("Helvetica", 24, "bold"), bg="white", fg="black")
title_label.pack(pady=(20, 10))

# Création de l'étiquette au-dessus de la liste déroulante
label = tk.Label(frame, text="Choisissez votre script", bg="white", fg="black")
label.pack(pady=10)

# Création de la Combobox pour sélectionner un script
scripts_combobox = ttk.Combobox(frame, width=30)
scripts_combobox.pack(pady=10)

# Charger les scripts lorsque l'utilisateur clique sur la liste déroulante
scripts_combobox.bind("<Button-1>", lambda event: load_scripts())

# Exécuter la fonction on_script_selected lorsque l'utilisateur sélectionne un script
scripts_combobox.bind("<<ComboboxSelected>>", on_script_selected)

# Bouton pour générer le rapport HTML
rapport_button = tk.Button(frame, text="Générer le Rapport HTML", command=generer_rapport, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
rapport_button.pack(pady=10)

# Lier l'événement de redimensionnement de la fenêtre à la fonction de redimensionnement
root.bind("<Configure>", resize_image)

# Exécution de la boucle principale
root.mainloop()
