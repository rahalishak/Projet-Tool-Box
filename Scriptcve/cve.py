import tkinter as tk
from tkinter import messagebox, ttk
import threading
import re
import os
import webbrowser
import nmap

NMAP_PATH = "C:/Program Files (x86)/Nmap/nmap.exe"

# Définir le répertoire de sauvegarde
result_directory = r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\result_cve"

# Vérifiez si Nmap est installé au chemin spécifié
if not os.path.exists(NMAP_PATH):
    print(f"Nmap executable not found at {NMAP_PATH}. Please check the path and try again.")
    exit(1)

def get_installed_versions(ip):
    versions = {}
    try:
        nm = nmap.PortScanner(nmap_search_path=(NMAP_PATH,))
        nm.scan(ip, arguments='-sV --script=vulners,version')
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = nm[host][proto].keys()
                for port in lport:
                    service = nm[host][proto][port]
                    product = service.get('product', '')
                    version = service.get('version', '')
                    cpe = service.get('cpe', '')
                    if 'script' in service:
                        for script_id, script_output in service['script'].items():
                            if 'vulners' in script_id:
                                vulns = extract_vulns_from_output(script_output)
                                versions[(proto, port)] = {
                                    'service': service['name'],
                                    'product': product,
                                    'version': version,
                                    'cpe': cpe,
                                    'vulns': vulns
                                }
    except Exception as e:
        print(f"Erreur lors de la récupération des versions : {e}")
    return versions

def extract_vulns_from_output(output):
    vulns = []
    lines = output.split('\n')
    for line in lines:
        match = re.search(r'(\S+)\s+(\d+\.\d+)\s+(https://vulners.com/\S+)', line)
        if match:
            cve = match.group(1)
            cvss = match.group(2)
            exploit = "EXPLOIT" in line
            vulns.append({'cve': cve, 'cvss': cvss, 'exploit': exploit})
    return vulns

def start_scan():
    ip = ip_entry.get()

    if not ip:
        messagebox.showerror("Erreur de Saisie", "Veuillez saisir une adresse IP.")
        return

    output_text.delete(1.0, tk.END)
    threading.Thread(target=run_scan, args=(ip,)).start()

def generate_html_report(ip, report_data):
    html_content = f"""
    <html>
    <head>
        <title>Rapport de Vulnérabilités CVE pour {ip}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #3498db; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Rapport de Vulnérabilités CVE pour {ip}</h1>
        <table>
            <tr>
                <th>Service</th>
                <th>Port</th>
                <th>Produit</th>
                <th>Version</th>
                <th>CVEs</th>
            </tr>
    """
    for (proto, port), details in report_data.items():
        cves = "<br>".join(f'<a href="https://vulners.com/cve/{cve["cve"]}" target="_blank">{cve["cve"]}</a>'
                           for cve in details['vulns'])
        html_content += f"""
        <tr>
            <td>{details['service']}</td>
            <td>{port}</td>
            <td>{details['product']}</td>
            <td>{details['version']}</td>
            <td>{cves}</td>
        </tr>
        """
    html_content += """
        </table>
    </body>
    </html>
    """
    return html_content

def run_scan(ip):
    output_text.insert(tk.END, f"Récupération des versions des logiciels installés sur {ip}...\n")
    versions = get_installed_versions(ip)
    if not versions:
        output_text.insert(tk.END, "Aucune version de logiciel récupérée.\n")
        return

    output_text.insert(tk.END, "Récupération des CVE...\n")
    report_data = {}
    for (proto, port), details in versions.items():
        output_text.insert(tk.END, f"Service : {details['service']}, Port : {port}\n")
        output_text.insert(tk.END, f"Produit : {details['product']}, Version : {details['version']}\n")
        report_data[(proto, port)] = details
        if details['vulns']:
            for vuln in details['vulns']:
                output_text.insert(tk.END, f"  CVE : {vuln['cve']} (CVSS : {vuln['cvss']})\n")
        else:
            output_text.insert(tk.END, "  Aucune CVE trouvée.\n")
        output_text.insert(tk.END, "\n")

    report_path = os.path.join(result_directory, "rapport_cve.html")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as report_file:
        report_file.write(generate_html_report(ip, report_data))
    output_text.insert(tk.END, f"Rapport généré et sauvegardé à l'adresse : {report_path}\n")

    if messagebox.askyesno("Ouvrir le Rapport", "Le rapport a été généré. Voulez-vous l'ouvrir ?"):
        webbrowser.open(f'file://{report_path}')

root = tk.Tk()
root.title("Scanner de Vulnérabilités CVE")
root.configure(bg='darkblue')

tk.Label(root, text="Adresse IP :", bg='darkblue', fg='white').grid(row=0, column=0, padx=10, pady=5)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=10, pady=5)

start_button = tk.Button(root, text="Démarrer Scan", command=start_scan, bg='#3498db', fg='white')
start_button.grid(row=2, column=0, columnspan=2, pady=10)

output_text = tk.Text(root, height=20, width=80, bg='lightgrey', fg='black')
output_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
