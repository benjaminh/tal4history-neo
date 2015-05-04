#!/usr/bin/env python3
# encoding: utf-8

import os
import re
import glob
import csv



#créer un dict avec clé = le nom du fichier .key sans extension (cad fichexxxx)  et valeurs = keywords contenu dans ce fichier
def create_dict_Keyword(keywordfilespath):
	mydict = {}
	keywordfilestyle = keywordfilespath + "/*.key"
	list_ficheskeywordnorm = glob.glob(keywordfilestyle)
	for fichekeywordnorm in list_ficheskeywordnorm:
		fichekeywordnorm_name = re.sub(r'keywords/', '', fichekeywordnorm)
		fichekeywordnorm_name = re.sub(r'\.key', '', fichekeywordnorm_name) 
		with open(fichekeywordnorm, 'r', encoding = 'utf8') as lafiche:
			keywords = lafiche.readlines()
			keywords = list(map(lambda s: re.sub(r'\n', '', s), keywords))
			mydict[fichekeywordnorm_name] = keywords
	return mydict


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

def del_inverse(dict_assoc):
    dict_sans_inverse = {}
    for clef,valeur in iter(dict_assoc.items()):
		    clef1,clef2 = clef.split('@')
		    clef_inverse = clef2+'@'+clef1
		    # Supprimer les relations inverses
		    for key,value in iter(dict_assoc.items()):
		        if (key == clef and clef_inverse not in output and value == valeur):
		            dict_sans_inverse[clef] = valeur
    return dict_sans_inverse

def calcul_ponderation(val1,val2):
    mini = min(val1,val2)
    maxi = max(val1,val2)
    ponderation = mini*mini/maxi 
    return ponderation
    
def creer_fichier_rel(dico):
	output = {}
	with open('keywords/relations_ponderees.csv', 'w', encoding = 'utf8') as relfile:
		for clef,valeur in iter(dico.items()):
		    fiche1,fiche2,motcle = clef.split('@')
		    clef_inverse = fiche2+'@'+fiche1+'@'+motcle
		    for key,value in iter(dico.items()):
		        if (key == clef_inverse and clef_inverse not in output):
		            ponderation_motclef = calcul_ponderation(valeur,value)
		            output[clef] = ponderation_motclef
		for rel_key,rel_value in iter(output.items()):
		    if (rel_value != 1):
		        a_ecrire = rel_key+'@'+str(rel_value)
		        print(a_ecrire)
		    #relfile.write(a_ecrire+'\n')
		


dossier_des_keyfiches = 'keywords' #dossier contenant les fiches de mot clef normalisées (en .key)
dictionnaire_des_motclefs = create_dict_Keyword(dossier_des_keyfiches)
listetemp = associationsDict(dictionnaire_des_motclefs)
creer_fichier_rel(listetemp)


