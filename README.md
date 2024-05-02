# Lutte Lombric

Projet final de CPA, M1 informatique : développement d'un jeu vidéo Worms-like. 

## Auteurs

- Adèle DESMAZIERES
- Thomas SANTONI

## Lancement

Depuis la racine du projet, lancer dans un terminal la commande suivante :

```sh
./src/main.py
```

Ou bien : 

```sh
python3 src/main.py
```

## Contrôles

Phase de déplacement

- Q, D : déplacement du ver à gauche et à droite
- ESPACE : saut vertical
- SHIFT GAUCHE/DROIT : passer à la phase de tir

Phase de tir

- Q, D : viser avec une arme à feu
- SHIFT GAUCHE/DROIT : changer d’arme
- BACKSPACE : retour à la phase de déplacement
- position de la souris : viser avec le téléporteur
- ESPACE maintenu : puissance du tir

## Objectif

L'objectif du jeu est de tuer tous les vers des adversaires avant de se faire tuer par eux ou par l'eau qui monte. Le jeu se joue en local à plusieurs joueurs. 