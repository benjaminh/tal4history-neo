#!/usr/bin/env python3
# encoding: utf-8

import os
import re
import Fichage
import CleanLaTeX
etape = 1

#renseigne ici le nom du fichier à cleaner en .tex
Fichier_a_traiter = 'memoireMQ.tex' 

Auteur_du_document = 'Matthieu Quantin' #prénom nom
Date_de_publication_du_document = '2014-06-04' # yyyy-mm-dd (format ISO8601 pour les date.)

##Options:
Mot_apres_la_derniere_fiche = 'CONCLUSION GÉNÉRALE' # pour écrire et arréter l'écriture de la dernière partie avant la conclusion... 
Taille_minimale = 150 #taille minimum d'une section pour en 'extraire' une fiche (en nombre de mots)
decoupe_paragraphe = False  #mettre "True" pour considérer les paragraphes comme des subsubsubsection et en faire des fiches, ou bien mettre "False" pour les laisser dans des fiches mères

##################################### 




etape += CleanLaTeX.AcoladeClose(Fichier_a_traiter, etape)
etape += CleanLaTeX.CrochetClose(Fichier_a_traiter, etape)
etape += CleanLaTeX.Clean(Fichier_a_traiter, etape)
Fichage.decoupe(Fichier_a_traiter, Mot_apres_la_derniere_fiche, Taille_minimale, etape, decoupe_paragraphe, Auteur_du_document, Date_de_publication_du_document)
