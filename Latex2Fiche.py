#!/usr/bin/env python3
# encoding: utf-8

import os
import re
import Fichage
import CleanLaTeX
etape = 0

#renseigne ici le nom du fichier à cleaner en .tex
Fichier_a_traiter = 'dieng_sa.tex' 

##Options:
Mot_apres_la_derniere_fiche = 'Conclusion générale' # pour écrire et arréter l'écriture de la dernière partie avant la conclusion... 
Taille_minimale = 150 #taille minimum d'une section pour en 'extraire' une fiche (en nombre de mots)
decoupe_paragraphe = True  #mettre "True" pour considérer les paragraphes comme des subsubsubsection et en faire des fiches, ou bien mettre "False" pour les laisser dans des fiches mères

##################################### 




etape += CleanLaTeX.AcoladeClose(Fichier_a_traiter, etape)
#etape += CleanLaTeX.CrochetClose(Fichier_a_traiter, etape)
etape += CleanLaTeX.Clean(Fichier_a_traiter, etape)
Fichage.decoupe(Fichier_a_traiter, Mot_apres_la_derniere_fiche, Taille_minimale, etape, decoupe_paragraphe)
