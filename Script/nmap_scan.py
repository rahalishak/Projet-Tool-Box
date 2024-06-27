import os
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import lxml.etree as ET
import time
import webbrowser

def list_machines():
    threading.Thread(target=_list_machines).start()

def _list_machines():
    start_progress_continuous()
    ip_range = ip_entry.get()
    try:
        process = subprocess.Popen(["nmap", "-sP", ip_range], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while process.poll() is None:
            time.sleep(0.1)
            root.after(0, update_progress)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise Exception(stderr)
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, stdout)
        messagebox.showinfo("Succès", "Le scan des machines disponibles est terminé.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du scan des machines : {e}")
    finally:
        stop_progress()

def scan_machine():
    threading.Thread(target=_scan_machine).start()

def _scan_machine():
    start_progress_continuous()
    ip_address = ip_entry.get()
    ports = port_entry.get()
    try:
        process = subprocess.Popen(["nmap", "-sV", "-sS", "-Pn", f"-p{ports}", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while process.poll() is None:
            time.sleep(0.1)
            root.after(0, update_progress)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise Exception(stderr)
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, stdout)
        messagebox.showinfo("Succès", "Le scan de la machine est terminé.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du scan de la machine : {e}")
    finally:
        stop_progress()

def generate_report():
    threading.Thread(target=_generate_report).start()

def _generate_report():
    try:
        start_progress_continuous()
        ip_address = ip_entry.get()
        ports = port_entry.get()

        report_dir = "C:\\Users\\ishak\\Documents\\ESI-2023-2024\\Projet-Tool-Box\\result_nmap"
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, "rapport.xml")
        xsl_path = "nmap.xsl"  # Adjust the path to your XSL file

        process = subprocess.Popen(["nmap", "-oX", report_path, "-sV", "-sS", "-sU", "-Pn", f"-p{ports}", ip_address],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while process.poll() is None:
            time.sleep(0.1)
            root.after(0, update_progress)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            raise Exception(stderr)

        if not os.path.exists(report_path):
            raise Exception(f"Le fichier XML {report_path} n'a pas été généré.")

        xml_tree = ET.parse(report_path)
        xsl_tree = ET.parse(xsl_path)
        transform = ET.XSLT(xsl_tree)
        result_tree = transform(xml_tree)
        html_report_path = os.path.join(report_dir, "rapport.html")
        result_tree.write(html_report_path, pretty_print=True, encoding='UTF-8')

        if messagebox.askyesno("Succès", f"Rapport HTML généré avec succès.\nChemin du rapport HTML : {html_report_path}\nVoulez-vous l'ouvrir ?"):
            webbrowser.open(f"file:///{html_report_path}")
        else:
            messagebox.showinfo("Information", f"Le rapport HTML est bien présent.\nChemin du rapport HTML : {html_report_path}")

    except Exception as e:
        print(f"Erreur: {e}")
        root.after(0, lambda: messagebox.showerror("Erreur", f"Erreur lors de la génération du rapport : {e}"))
    finally:
        stop_progress()

def get_nmap_version():
    result = subprocess.run(["nmap", "--version"], capture_output=True, text=True)
    version_info = result.stdout.split('\n')[0]
    return version_info

def start_progress():
    progress_bar['value'] = 0
    progress_label['text'] = "Progress: 0%"

def stop_progress():
    progress_bar['value'] = 100
    progress_label['text'] = "Progress: 100%"

def start_progress_continuous():
    progress_bar['value'] = 0
    progress_label['text'] = "Progress: 0%"
    root.after(100, update_progress)

def update_progress():
    current_value = progress_bar['value']
    if current_value < 100:
        new_value = current_value + 1
        if new_value > 100:
            new_value = 100
        progress_bar['value'] = new_value
        progress_label['text'] = f"Progress: {new_value}%"
        root.after(100, update_progress)

# Interface utilisateur Tkinter
root = tk.Tk()
root.title("Nmap GUI")
root.configure(bg='navy')

# Version info
version_info = get_nmap_version()
tk.Label(root, text=version_info, font=("Helvetica", 10, "italic"), bg='navy', fg='white').grid(row=0, column=0, columnspan=2, pady=5)

# IP address entry
tk.Label(root, text="Adresse IP :", font=("Helvetica", 12), bg='navy', fg='white').grid(row=1, column=0, sticky="e", padx=5, pady=5)
ip_entry = tk.Entry(root)
ip_entry.grid(row=1, column=1, padx=5, pady=5)

# Ports entry
tk.Label(root, text="Ports (séparés par des virgules) :", font=("Helvetica", 12), bg='navy', fg='white').grid(row=2, column=0, sticky="e", padx=5, pady=5)
port_entry = tk.Entry(root)
port_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
button_frame = tk.Frame(root, bg='navy')
button_frame.grid(row=3, column=0, columnspan=2, pady=10)

button_style = {"width": 15, "font": ("Helvetica", 10), "bg": "dodgerblue", "fg": "white"}

tk.Button(button_frame, text="Détection de machines", command=list_machines, **button_style).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Scan d'une machine", command=scan_machine, **button_style).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Génération d'un rapport détaillé", command=generate_report, **button_style).grid(row=0, column=2, padx=5)

# Text area
text_area = tk.Text(root, wrap=tk.WORD, width=60, height=15)
text_area.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Progress bar
progress_bar = ttk.Progressbar(root, mode='determinate', maximum=100)
progress_bar.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

# Progress label
progress_label = tk.Label(root, text="Progress: 0%", font=("Helvetica", 12), bg='navy', fg='white')
progress_label.grid(row=6, column=0, columnspan=2, pady=5)

# Quit button
quit_button = tk.Button(root, text="Quitter", command=root.destroy, bg='red', fg='white')
quit_button.grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
