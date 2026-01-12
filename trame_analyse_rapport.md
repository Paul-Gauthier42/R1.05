# Rapport d'analyse réseau : trame_analyse

Ce rapport regroupe des informations utiles pour détecter de potentielles attaques (SYN flood / DDoS, port scan, scans basés sur les flags TCP).

## IP avec le plus grand nombre de ports touchés

- IP suspecte (port scan possible) : **BP-Linux8**
- Nombre total de ports touchés (paquets) : **2968**

## Répartition des principaux flags TCP

| Flag | Nombre de paquets |
|------|-------------------|
| SYN | 2092 |
| PSH | 1673 |
| FIN | 40 |

## Top services par nombre de SYN (potentiel SYN flood / DDoS)

| Service (dst_ip:port) | Nombre de SYN |
|------------------------|---------------|
| 184.107.43.74:http | 2000 |
| mauves.univ-st-etienne.fr:https | 7 |
| par21s17-in-f1.1e100.net:https | 6 |
| par21s23-in-f3.1e100.net:https | 6 |
| www.aggloroanne.fr:https | 6 |
| par21s05-in-f131.1e100.net:http | 5 |
| par21s23-in-f10.1e100.net:https | 4 |
| par21s20-in-f14.1e100.net:https | 2 |
| par21s17-in-f14.1e100.net:https | 2 |
| 201.181.244.35.bc.googleusercontent.com:https | 1 |

## Top IP source par nombre total de ports touchés (port scan)

| IP source | Nombre total de ports (paquets) |
|-----------|----------------------------------|
| BP-Linux8 | 2968 |
| www.aggloroanne.fr | 2130 |
| 190-0-175-100.gba.solunet.com.ar | 2000 |
| mauves.univ-st-etienne.fr | 1687 |
| par10s38-in-f3.1e100.net | 827 |
| par21s23-in-f3.1e100.net | 251 |
| par21s04-in-f4.1e100.net | 223 |
| par21s17-in-f1.1e100.net | 180 |
| par21s23-in-f10.1e100.net | 99 |
| 192.168.190.130 | 66 |

## Top IP source par nombre de paquets

| IP source | Nombre de paquets |
|-----------|-------------------|
| BP-Linux8 | 2968 |
| www.aggloroanne.fr | 2130 |
| 190-0-175-100.gba.solunet.com.ar | 2000 |
| mauves.univ-st-etienne.fr | 1687 |
| par10s38-in-f3.1e100.net | 827 |
| par21s23-in-f3.1e100.net | 251 |
| par21s04-in-f4.1e100.net | 223 |
| par21s17-in-f1.1e100.net | 180 |
| par21s23-in-f10.1e100.net | 99 |
| 192.168.190.130 | 66 |

## Top IP destination par nombre de paquets

| IP destination | Nombre de paquets |
|----------------|-------------------|
| BP-Linux8 | 5798 |
| 184.107.43.74 | 2000 |
| www.aggloroanne.fr | 1022 |
| mauves.univ-st-etienne.fr | 751 |
| par10s38-in-f3.1e100.net | 255 |
| par21s23-in-f3.1e100.net | 200 |
| par21s17-in-f1.1e100.net | 176 |
| par21s23-in-f10.1e100.net | 85 |
| par21s04-in-f4.1e100.net | 79 |
| 192.168.190.130 | 60 |

## Top 5 IP source par nombre de SYN (SYN seuls)

| IP source | Nombre de SYN |
|-----------|---------------|
| 190-0-175-100.gba.solunet.com.ar | 2000 |
| BP-Linux8 | 46 |
| mauves.univ-st-etienne.fr | 7 |
| par21s17-in-f1.1e100.net | 6 |
| par21s23-in-f3.1e100.net | 6 |

IP la plus active en SYN seuls : **190-0-175-100.gba.solunet.com.ar** avec **2000** paquets.

## Évolution du nombre de paquets dans le temps

Un graphique en courbe est disponible dans le rapport HTML pour visualiser le nombre de paquets par seconde.

