import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
import re


# ================== PARSING DES LIGNES TCPDUMP ===================

regex_ligne_ip = re.compile(
    r'^(?P<time>\d{2}:\d{2}:\d{2}\.\d+)\s+IP\s+'
    r'(?P<src>[^ ]+)\s+>\s+(?P<dst>[^:]+):\s+'
    r'Flags\s+\[(?P<flags>[^\]]+)\],\s+'
    r'seq\s+(?P<seq>[0-9:]+),\s+'
    r'ack\s+(?P<ack>\d+),\s+'
    r'win\s+(?P<win>\d+),.*?'
    r'length\s+(?P<length>\d+)'
)


def split_ip_port(value: str):
    if "." not in value:
        return value, ""
    host, port = value.rsplit(".", 1)
    return host, port


def parse_ligne_ip(ligne: str):
    m = regex_ligne_ip.match(ligne.strip())
    if not m:
        return None

    d = m.groupdict()
    champs_obligatoires = ["time", "src", "dst", "flags", "seq", "ack", "win", "length"]
    if any(not d.get(c) for c in champs_obligatoires):
        return None

    src_ip, src_port = split_ip_port(d["src"])
    dst_ip, dst_port = split_ip_port(d["dst"])

    return {
        "time": d["time"],
        "src_ip": src_ip,
        "src_port": src_port,
        "dst_ip": dst_ip,
        "dst_port": dst_port,
        "flags": d["flags"],
        "seq": d["seq"],
        "ack": d["ack"],
        "win": d["win"],
        "length": d["length"],
    }


def analyser_fichier_trame(chemin_entree: str, chemin_csv: str):
    with open(chemin_entree, "r", encoding="utf-8") as f_in, \
         open(chemin_csv, "w", newline="", encoding="utf-8") as f_out:

        writer = csv.writer(f_out, delimiter=",")
        writer.writerow([
            "time", "src_ip", "src_port",
            "dst_ip", "dst_port",
            "flags", "seq", "ack", "win",
            "length"
        ])

        current = None

        for ligne in f_in:
            parsed = parse_ligne_ip(ligne)
            if parsed:
                if current is not None:
                    writer.writerow([
                        current["time"],
                        current["src_ip"],
                        current["src_port"],
                        current["dst_ip"],
                        current["dst_port"],
                        current["flags"],
                        current["seq"],
                        current["ack"],
                        current["win"],
                        current["length"],
                    ])
                current = parsed
            else:
                # On ignore complètement les lignes hexdump ou autres
                continue

        if current is not None:
            writer.writerow([
                current["time"],
                current["src_ip"],
                current["src_port"],
                current["dst_ip"],
                current["dst_port"],
                current["flags"],
                current["seq"],
                current["ack"],
                current["win"],
                current["length"],
            ])


# ================== INTERFACE TKINTER ===================

def choisir_fichier():
    chemin_fichier = filedialog.askopenfilename(
        title="Sélectionner un fichier de trames",
        filetypes=[("Fichiers texte", "*.txt *.log *.out"), ("Tous les fichiers", "*.*")]
    )
    if chemin_fichier:
        label_chemin.config(text=f"Fichier sélectionné : {chemin_fichier}")
        try:
            dossier, nom = os.path.split(chemin_fichier)
            nom_sans_ext, _ = os.path.splitext(nom)
            chemin_csv = os.path.join(dossier, nom_sans_ext + "_analyse.csv")

            analyser_fichier_trame(chemin_fichier, chemin_csv)

            messagebox.showinfo(
                "Terminé",
                f"Fichier CSV créé :\n{chemin_csv}"
            )
        except Exception as e:
            messagebox.showerror(
                "Erreur",
                f"Problème lors de la conversion : {e}"
            )
    else:
        label_chemin.config(text="Aucun fichier sélectionné")


def quitter():
    fenetre.destroy()


fenetre = tk.Tk()
fenetre.title("Analyse de trames -> CSV")
fenetre.geometry("500x220")

btn_choisir_fichier = tk.Button(fenetre, text="Choisir un fichier", command=choisir_fichier)
btn_choisir_fichier.pack(pady=20)

label_chemin = tk.Label(fenetre, text="Aucun fichier sélectionné", wraplength=460)
label_chemin.pack(pady=20)

btn_quitter = tk.Button(fenetre, text="Quitter", command=quitter)
btn_quitter.pack(pady=20)

fenetre.mainloop()
