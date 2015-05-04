#!/usr/bin/env python3
# encoding: utf-8

import math
import os
import re
import glob
import csv

# a apartir d'un id de fiche du type 'fiche1.2.4' compte le nombre de mot contenu dans le fichier correspondant /fiches/fiche1.2.4.txt
def compte_mots(unefiche):
    fichierfiche = 'fiches/' + unefiche + '.txt'
    with open(fichierfiche, 'r', encoding = 'utf8') as lafiche:
        text = lafiche.read()
        separateur = re.compile(r'\W+',re.U)
        liste_mots = separateur.split(text)
        nb_mots = len(liste_mots)
    return nb_mots
    
#créer un dict avec clé = le nom du fichier .key sans extension (cad fichexxxx)  et valeurs = keywords contenu dans ce fichier
#calcul l'idf (inverse document frequency) c'est à dire que idf est grand si le mot-clef est secifique à une fiche et n'apparait pas ou peu dans les autres.
def create_dict_Keyword(keywordfilespath):
    mydict = {}
    idf_dict = {}
    idf_temp_dict = {}
    nb_fiches = 0
    keywordfilestyle = keywordfilespath + "/*.key"
    list_ficheskeywordnorm = glob.glob(keywordfilestyle)
    
    for fichekeywordnorm in list_ficheskeywordnorm:
        nb_fiches += 1
        fichekeywordnorm_name = re.sub(r'keywords/', '', fichekeywordnorm)
        fichekeywordnorm_name = re.sub(r'\.key', '', fichekeywordnorm_name) 
        with open(fichekeywordnorm, 'r', encoding = 'utf8') as lafiche:
            #dictionnaire fiche-motsclefs associés
            keywords = lafiche.readlines()
            keywords = list(map(lambda s: re.sub(r'\n', '', s), keywords))
            mydict[fichekeywordnorm_name] = keywords
            #compte le nombre de documents dans lequel chaque mot-clef est présent
            keywords = set(keywords) # on ne veut compter qu'une seule fois le mot clef par fiche
            for keyword in keywords:
                if keyword not in idf_temp_dict:
                    idf_temp_dict[keyword] = 1 #ajoute le mot-clef s'il n'est pas dans le dict idf
                else:
                    idf_temp_dict[keyword] += 1 #incrémente le nombre de documents dans lequel ce mot clef est présent (pour calculer l'idf on attend de savoir combien de documents on a)
    #calcul l'idf. 
    for key, valeur in iter(idf_temp_dict.items()):
        idf = math.log10(nb_fiches/valeur)
        idf_dict[key] = idf
    return mydict, idf_dict


#créer un dictionnaire, chaque "ligne" signale 2 fiches ayant un mot clef en commun. (liens en double car match aller et retour)
def associationsDict(dictRel):
    dict_assoc = {}
    for clef, valeurs in iter(dictRel.items()):
        for valeur in valeurs:
            for clef2, valeurs2 in iter(dictRel.items()):
                if (valeur in valeurs2 and clef2 != clef):
                    dict_key = clef+'@'+clef2+'@'+valeur
                    if (dict_key in dict_assoc):
                        dict_assoc[dict_key] += 1
                    else:
                        dict_assoc[dict_key] = 1
    # On obtient un dictionnaire du type 'fiche1@fiche2@motcle': occurrence_motcle_fiche1
    # On obtient également les occurrences opposées: 'fiche2@fiche1@motcle': occurrence_motcle_fiche2
    return dict_assoc

#fonction OBSOLETE pour supprimer les occurences inverse dans un dictionnaire
#def del_inverse(dict_assoc):
#    dict_sans_inverse = {}
#    for clef,valeur in iter(dict_assoc.items()):
#            clef1,clef2 = clef.split('@')
#            clef_inverse = clef2+'@'+clef1
#            # Supprimer les relations inverses
#            for key,value in iter(dict_assoc.items()):
#                if (key == clef and clef_inverse not in output and value == valeur):
#                    dict_sans_inverse[clef] = valeur
#    return dict_sans_inverse

#construit un dictionnaire avec les mots-clefs normalisés associés à leur nombre occurence dans l'ensemble du fichier source (le mémoire). Ce nombre est écrit dans le fichier (obtenu par TAL)
def dict_extractions(fichier_des_mots_extraits):
    with open(fichier_des_mots_extraits, 'rt', encoding = 'utf8') as keywordFile:
        dict_extraction_occurence = {}
        extraction = csv.reader(keywordFile, delimiter='\t', quotechar='"')
        for row in extraction:
            occurence = row[0]
            mot_norm = row[1].lower()
            dict_extraction_occurence[mot_norm] = occurence
        print(str(dict_extraction_occurence))
    return dict_extraction_occurence

# calcul une pondération tf-idf à pour chaque lien entre 2 fiches.
def calcul_ponderation(key,val1,val2, dict_extraction_occurences, idf_dict):
    fiche1,fiche2,motcle = key.split('@')
    occurence_globale_motclef = dict_extraction_occurences[motcle]
    occurences_2fiches = val1 + val2
    nb_mots_2fiches = compte_mots(fiche1) + compte_mots(fiche2)
    idf_mot = idf_dict[motcle]
    tf = occurences_2fiches / nb_mots_2fiches
    ponderation = tf * idf_mot
    return ponderation
    
#à partir d'un dictionnaire du type 'fiche1@fiche2@motcle': occurrence_motcle_fiche1' (fonction associationsDict)
#cette fonction va créer un dictionnaire 'fiche1@fiche2@ponderation_du_lien_par_idf'
def creer_fichier_rel(dico, dict_extraction_occurences, idf_dict):
    output = {}
    with open('keywords/relations_ponderees.csv', 'w', encoding = 'utf8') as relfile:
        for clef,valeur in iter(dico.items()):
            fiche1,fiche2,motcle = clef.split('@')
            clef_inverse = fiche2+'@'+fiche1+'@'+motcle
            for key,value in iter(dico.items()):
                if (key == clef_inverse and clef_inverse not in output):
                    ponderation_motclef = calcul_ponderation(clef,valeur,value, dict_extraction_occurences, idf_dict)
                    output[clef] = ponderation_motclef
        for rel_key,rel_value in iter(output.items()):
            a_ecrire = rel_key+'@'+str(rel_value)
            print(a_ecrire)
            #relfile.write(a_ecrire+'\n')
        


dossier_des_keyfiches = 'keywords' #dossier contenant les fiches de mot clef normalisées (en .key)
nom_du_fichier_des_mots_extraits_par_tal = 'memoireMQkey.csv' #fichier contenant tous les mots-clefs extratits du mémoire par TAL,  avec en 1ere colonne les occurences de chaque mot dans le memoire.

dict_extraction_occurences = dict_extractions(nom_du_fichier_des_mots_extraits_par_tal)
dictionnaire_des_motclefs, idf_dictionnaire = create_dict_Keyword(dossier_des_keyfiches)
dicttemp = associationsDict(dictionnaire_des_motclefs)
creer_fichier_rel(dicttemp, dict_extraction_occurences, idf_dictionnaire)


