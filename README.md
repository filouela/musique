# Création d'une partition à partir d'un fichier audio

## Présentation

Ce projet a été réalisé dans le cadre d'un TIPE en groupe.

L'objectif est de retranscrire un signal sonore en partition. Le résultat final est une partition générée puis compilée automatiquement au format PDF à l'aide de LaTeX.

---

## Principe de fonctionnement

Le programme suit les étapes suivantes :

### 1. Chargement du fichier audio et détection des notes

Le fichier audio à retranscrire doit être au format WAV.

Un filtre passe-bas est appliqué sur le signal afin de trouver les attaques et extinctions des notes, ie de trouver quand les notes sont jouées. On peut alors découper le signal pour isoler chacune des notes.

### 2. Détermination des fréquences fondamentales et des temps

Pour chaque note isolée :
* une transformée de Fourier rapide (FFT) est calculée ;
* la fréquence correspondant à l'amplitude maximale est considérée comme la fréquence fondamentale de la note.

### 3. Identification des notes

Des fréquences fondamentales, on calcule :
* le nombre de demi-tons par rapport au Do central (261,626 Hz) ;
* l'octave correspondante.

### 4. Calcul du rythme

Les notes sont regroupées selon leurs durées. La durée la plus représentée représente le rythme de référence (de valeur 1).

Les autres durées sont assimilées à un rythme normalisé par rapport au rythme de référence.

### 5. Détermination de quelques paramètres suplémentaires pour la partition

Le programme calcule la clé et l'armure de la musique.

L'armure calculée est celle qui minimise le nombre de notes étrangères à la gamme et la clé choisie est celle qui correspond le mieux à la hauteur de la mélodie (clé de Sol pour des mélodies aigües, clé de Fa pour des mélodies graves).

### 6. Génération de la partition

Tous les paramètres calculés sont convertis au format ABC. Une partition complète est alors construite automatiquement et un fichier PDF est produit.

---

## Outils nécessaires

### Python

Le programme a besoin des bibliothèques suivantes :
```text
numpy
scipy
matplotlib
math
sys
```

### LaTeX, Inkscape et abcM2PS

Le logiciel `abcm2ps` est utilisé pour convertir les partitions ABC en SVG.

La partition est générée grâce à LaTeX et Inkscape.

Dans le fichier `vierge.tex` est écrit un chemin pour Inkscape, à adapter :
```latex
\svgsetup{
  inkscapeexe=/Applications/Inkscape.app/Contents/MacOS/inkscape
}
```

---

## Arborescence minimale

```text
Projet/
│
├── assets/
│   ├── vierge.tex
│   └── newfile.tex
│
├── scores/
│
├── tex_2_abc.py
├── main.py
├── filtrage.py
├── abcd.py
│
└── audio.wav
```

Le dossier `scores` doit exister avant l'exécution.

---

## Limites

Le programme fait preuve de limites :
* il ne permet pas de détecter correctement plusieurs notes quand elles sont jouées à la fois (mais une amélioration est possible avec le travail de mes camarades) ;
* pour avoir de meilleurs résultats, il est crucial de modifier `facteur_frequence_coupure` selon le tempo du morceau, mais il n'est actuellement pas possible de le modifier automatiquement ;
* pour la détermination de la note, la fréquence de l'amplitude maximale est considérée, alors que l'amplitude du fondamental n'est pas toujours maximale.

Les résultats sont meilleurs pour des mélodies lentes ou modérément rapides, jouées avec un seul instrument.
