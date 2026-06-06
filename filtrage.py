""" BIBLIOTHEQUES """
from scipy.signal import butter, filtfilt
import numpy as np



""" FONCTIONS """
# Fonction de filtrage passe-bas
def filtre_passe_bas(signal, echantillonnage, facteur_frequence_coupure, ordre_filtre):
    frequence_coupure = facteur_frequence_coupure / (0.5 * echantillonnage)
    # Normaliser la fréquence de coupure (pour butter)
    coeff_appliques_entree, retroaction = butter(ordre_filtre, frequence_coupure, btype='low')
    # Conçoit un filtre de type btype ; coeff_appliques_entree : coeff appliqués à l'entrée ; retroaction : rétroaction
    module_signal = np.abs(signal)
    signal_filtre = filtfilt(coeff_appliques_entree, retroaction, module_signal)
    return signal_filtre
