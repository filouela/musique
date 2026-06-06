""" BIBLIOTHEQUES """
import numpy as np
import math
import filtrage
import matplotlib.pyplot as plt
import scipy



""" PARAMETRES """
# Paramètres du filtre
ordre_filtre = 4  # Ordre du filtre
facteur_frequence_coupure = 1.1  # Fréquence de coupure en Hz

liste_nb_demi_tons = np.array(
    [
        [0, 2, 4, 5, 7, 9, 11], # 
        [0, 2, 4, 6, 7, 9, 11], # dièses : fa
        [1, 2, 4, 6, 7, 9, 11], # fa, do
        [1, 2, 4, 6, 8, 9, 11], # fa, do, sol
        [1, 3, 4, 6, 8, 9, 11], # fa, do, sol, ré
        [1, 3, 4, 6, 8, 10, 11], # fa, do, sol, ré, la
        [1, 3, 5, 6, 8, 10, 11], # fa, do, sol, ré, la, mi
        [1, 3, 5, 6, 8, 10, 0], # fa, do, sol, ré, la, mi, si
        [0, 2, 3, 5, 7, 9, 10], # bémols : si
        [0, 2, 3, 5, 7, 9, 10], # si, mi
        [0, 2, 3, 5, 7, 8, 10], # si, mi, la
        [0, 1, 3, 5, 7, 8, 10], # si, mi, la, ré
        [0, 1, 3, 5, 6, 8, 10], # si, mi, la, ré, sol
        [11, 1, 3, 5, 6, 8, 10], # si, mi, la, ré, sol, do
        [11, 1, 3, 4, 6, 8, 10], # si, mi, la, ré, sol, do, fa
	]
)
liste_armure = ["C", "G", "D", "A", "E", "B", "^F", "^C", "F", "Bb", "Eb", "Ab", "Db", "Gb", "Cb"]



""" OUTILS """
def trouver_indice_minimum(liste) :
    indice = 0
    minimum = liste[0]
    for i, elt in enumerate(liste):
        if elt < minimum :
            minimum = elt
            indice = i
    return(indice)

def afficher_signal(signal, signal_lisse) :
    plt.plot(signal, color = 'c', label="Signal originel")
    plt.plot(signal_lisse, color = 'r', label="Signal lissé")
    plt.title("Lissage de la courbe")
    plt.xlabel("Echantillons")
    plt.ylabel("Amplitude du signal")
    plt.legend()
    plt.show()



""" FONCTIONS """
# Charger le fichier audio
def charger_audio (file_name) :
    frequence_echantillonnage, data_audio = scipy.io.wavfile.read(file_name)
    if data_audio.ndim > 1:
        signal = data_audio[:, 0]
    else:
        signal = data_audio
    return signal, frequence_echantillonnage

# Appliquer la détection d'enveloppe (lisser le signal)
def lisser_signal(signal, frequence_echantillonnage) :
    signal_lisse = filtrage.filtre_passe_bas(signal, frequence_echantillonnage, facteur_frequence_coupure, ordre_filtre)
    signal_lisse = filtrage.filtre_passe_bas(signal_lisse, frequence_echantillonnage, facteur_frequence_coupure, ordre_filtre)
    return signal_lisse

# Fenêtrage du signal (on "capture" chaque note dans une fenêtre)
def fenetrage(signal, signal_lisse):
    n = len(signal_lisse)
    liste_fenetres = []
    fenetre = []
    i = 0
    while i < n - 1 :
        # Croissance de la courbe du signal
        while i < n - 1 and signal_lisse[i] <= signal_lisse[i + 1] :
            fenetre.append(signal[i])
            i += 1
        # Décroissance de la courbe du signal
        if i < n - 1 and signal_lisse[i] > signal_lisse[i + 1] :
            while i < n - 1 and signal_lisse[i] > signal_lisse[i + 1] :
                fenetre.append(signal[i])
                i += 1
            fenetre = np.array(fenetre)
            liste_fenetres.append(fenetre)  # on a passé une montagne (= note), on a donc atteint la fin de la fenêtre
            fenetre = []
    return liste_fenetres

# Renvoie la liste des fondamentaux (= des notes jouées) du signal
def trouver_fondamentaux(frequence_echantillonnage, liste_fenetres) :
    liste_fondamentaux = []
    for fenetre in liste_fenetres :
        n = len(fenetre)
        fenetre_coupee = fenetre[0:3*n//4]
        amplitude = scipy.fft.fft(fenetre_coupee)
        frequence = scipy.fft.fftfreq(len(fenetre_coupee), d=1/frequence_echantillonnage)
        fondamentali = np.argmax(np.abs(amplitude)) # on fait l'hypothèse que le fondamental correspond à la fréquence d'amplitude maximale
        # (np.argmax renvoie un indice)
        liste_fondamentaux.append(frequence[fondamentali])
    return liste_fondamentaux

# Renvoie la note et son octave correspondant à la fréquence donnée
def frequence_to_nb_demi_tons_octave(freq):
    """""""""""""""
    Entrée : fréquence (Hz)

    Sortie : le nombre de demi-tons séparant la note d'un do, l'octave de la note (0 de référénce : octave 3)
    """""""""""""""
    if freq.dtype == np.dtype('O') : return (0, 0)
    nb_demi_tons = int(np.round((math.log2(freq/261.626) * 12)))
    octave = nb_demi_tons // 12
    return nb_demi_tons % 12, octave

# Calcul de l'octave moyenne (trouver la clé de la partition)
def moyenne_octaves(liste_notes) :
    octave_moyenne = np.mean([octave for (demi_tons, octave) in liste_notes])
    if octave_moyenne < 0 :
        return 'clef=F octave=-1'
    return 'clef=G'

# Calcul de l'armure du morceau
def trouver_armure(liste_notes) :
	distance_armure_morceau = np.zeros(len(liste_nb_demi_tons))
	i = 0
	for armure in liste_nb_demi_tons :
		for (nb_demi_tons, octave) in liste_notes :
			if (not(nb_demi_tons in armure)) :
				distance_armure_morceau[i] += 1
		i += 1
    # pour chaque armure, on regarde le nombre de demi-tons qu'elle a en commun avec le morceau
	armure_min = trouver_indice_minimum(distance_armure_morceau)
	return(armure_min)

# Trouver les durées des notes
def trouver_durees(signal, liste_fenetres):
    notes = [np.argmax(fenetre) for fenetre in liste_fenetres]
    durees = [notes[i+1] - notes[i] + len(liste_fenetres[i]) for i in range(0, len(notes) - 1)]
    durees.append(len(signal) - notes[len(notes) - 1])
    return durees

# Ranger les durées selon les rythmes
def trier_durees(liste_durees) :
    liste_categories = []
    for k, duree in enumerate(liste_durees) :
        trouve = False
        for i in range(0, len(liste_categories)) :
            (duree_min, duree_max, indices) = liste_categories[i]
            if duree_min * 0.8 <= duree <= duree_max * 1.2 :
                duree_min = min(duree_min, duree)
                duree_max = max(duree_max, duree)
                indices.append(k)
                liste_categories[i] = (duree_min, duree_max, indices)
                trouve = True
        if trouve == False :
             liste_categories.append((duree, duree, [k]))
    return liste_categories

# Trouver le rythme de référence
def trouver_rythme_ref(liste_durees, liste_categories) :
    occurence_max = 0
    for (duree_min, duree_max, indices) in liste_categories :
        if len(indices) > occurence_max :
            occurence_max = len(indices)
            rythme_ref = np.mean(np.array([liste_durees[i] for i in indices]))
    return rythme_ref

# Trouver les rythmes
def trouver_rythmes(liste_durees, rythme_ref) :
    rapports_rythmes_partition = ["1/8", "1/4", "1/3", "1/2", "1", "3/2", "2", "3", "4"]
    rapports_rythmes = [1/8, 1/4, 1/3, 1/2, 1, 3/2, 2, 3, 4]
    liste_rythmes = []
    for duree in liste_durees :
        best_result = 1000
        meilleur_rapport = ""
        for i in range(0, len(rapports_rythmes)) :
            result = (duree / rapports_rythmes[i])/rythme_ref
            if abs(result - 1) < best_result :
                best_result = abs(result - 1)
                meilleur_rapport = rapports_rythmes_partition[i]
        liste_rythmes.append(meilleur_rapport)
    return(liste_rythmes)

# Passer des caractéristiques de la note à la partition
def note_to_partition(nb_demi_tons, octave, rythme, armure) :
    notes = ["C" if armure[0] == 0 else "=C" if armure[0] == 1 else "=C",
            "^C" if armure[0] == 0 else "C" if armure[0] == 1 else "D",
            "D" if armure[1] == 2 else "=D" if armure[1] == 3 else "=D",
            "^D" if armure[1] == 2 else "D" if armure[1] == 3 else "E",
            "E" if armure[2] == 4 else "=E" if armure[2] == 2 else "=E",
            "F" if armure[3] == 5 else "=F" if armure[3] == 6 else "=F",
            "^F" if armure[3] == 5 else "F" if armure[3] == 6 else "G",
            "G" if armure[4] == 7 else "=G" if armure[4] == 8 else "=G",
            "^G" if armure[4] == 7 else "G" if armure[4] == 8 else "A",
            "A" if armure[5] == 9 else "=A" if armure[5] == 10 else "=A",
            "^A" if armure[5] == 9 else "A" if armure[5] == 10 else "B",
            "B" if armure[6] == 11 else "=B" if armure[6] == 0 else "=B"]
    n = notes[nb_demi_tons]
    o = "" if octave == 0 else "'"*octave if octave > 0 else ","*np.abs(octave)
    nom = f"{n}{o}{rythme}"
    return nom

def to_partition(liste_notes, liste_rythmes, armure) :
    score = ""
    for k, (note, octave) in enumerate(liste_notes) :
        if k % 4 == 0 :
            score += "|"
        score += note_to_partition(note, octave, liste_rythmes[k], armure)
    return (score)

def main(file_name) :
    signal, frequence_echantillonnage = charger_audio(file_name)
    signal_lisse = lisser_signal(signal, frequence_echantillonnage)
    liste_fenetres = fenetrage(signal, signal_lisse)
    liste_frequences = trouver_fondamentaux(frequence_echantillonnage, liste_fenetres)
    liste_notes = [frequence_to_nb_demi_tons_octave(frequence) for frequence in liste_frequences]
    indice_amure = trouver_armure(liste_notes)
    armure = liste_nb_demi_tons[indice_amure]
    K = liste_armure[indice_amure]
    octave = moyenne_octaves(liste_notes)
    liste_durees = trouver_durees(signal, liste_fenetres)
    liste_categories = trier_durees(liste_durees)
    rythme_ref = trouver_rythme_ref(liste_durees, liste_categories)
    liste_rythmes = trouver_rythmes(liste_durees, rythme_ref)
    score = to_partition(liste_notes, liste_rythmes, armure)
    return(K, octave, score)
