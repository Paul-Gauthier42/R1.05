import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import os
import re

# ================== PARSING DES LIGNES TCPDUMP ===================

# Exemple de ligne visée :
# 15:34:04.766656 IP BP-Linux8.ssh > 192.168.190.130.50019: Flags [P.], seq 2243505564:2243505672, ack 1972915080, win 312, options [...], length 108
regex_ligne_ip = re.compile(
    r'^(?P<time>\d{2}:\d{2}:\d{2}\.\d+)\s+IP\s+'
    r'(?P<src>[^ ]+)\s+>\s+(?P<dst>[^:]+):\s+'
    r'Flags\s+\[(?P<flags>[^\]]+)\],\s+'
    r'seq\s+(?P<seq>[0-9:]+),\s+'
    r'ack\s+(?P<ack>\d+),\s+'
    r'win\s+(?P<win>\d+),.*?'
    r'length\s+(?P<length>\d+)'
)

def split_ip_port(value):
    """
    Sépare '192.168.190.130.50019' en ('192.168.190.130', '50019')
    ou 'BP-Linux8.ssh' en ('BP-Linux8', 'ssh').
    On coupe uniquement sur le dernier '.' car les IP en ont déjà plusieurs. [web:85]
    """
    if "." not in value:
        return value, ""
    host, port = value.rsplit(".", 1)
    return host, port

def parse_ligne_ip(ligne):
    m = regex_ligne_ip.match(ligne.strip())
    if not m:
        return None
    d = m.groupdict()

    # src et dst sont de la forme "hote.port"
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

def analyser_fichier_trame(chemin_entree, chemin_csv):
    """
    Lit un fichier texte contenant les trames tcpdump + hexdump
    et écrit un CSV avec une ligne par paquet. [web:71][web:80]
    """
    with open(chemin_entree, "r", encoding="utf-8") as f_in, \
         open(chemin_csv, "w", newline="", encoding="utf-8") as f_out:

        writer = csv.writer(f_out, delimiter=",")
        writer.writerow([
            "time", "src_ip", "src_port",
            "dst_ip", "dst_port",
            "flags", "seq", "ack", "win",
            "length", "hex_dump"
        ])

        current = None

        for ligne in f_in:
            # Nouvelle ligne IP ?
            parsed = parse_ligne_ip(ligne)
            if parsed:
                # Si on avait déjà une trame en cours, on l'écrit
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
                        " ".join(current["hex_dump"]),
                    ])
                # On commence une nouvelle trame
                current = parsed
                current["hex_dump"] = []
            else:
                # Ligne hex ? (0x0000: ...)
                if current is not None and ligne.strip().startswith("0x"):
                    try:
                        _, hexa = ligne.split(":", 1)
                        current["hex_dump"].append(hexa.strip())
                    except ValueError:
                        pass

        # Dernière trame
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
                " ".join(current["hex_dump"]),
            ])

# ================== INTERFACE TKINTER ===================

def choisir_fichier():
    chemin_fichier = filedialog.askopenfilename(
        title="Sélectionner un fichier de trames"
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
