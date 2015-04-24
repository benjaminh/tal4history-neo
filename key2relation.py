#!/usr/bin/env python3
# encoding: utf-8

import os
import re
import glob
import csv



#créer un dict avec clée = le nom du fichier .key sans extension (cad fichexxxx)  et valeurs = keywords contenu dans ce fichier
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


#créer un tableau, chaque "ligne" signale 2 fiches ayant un mot clef en commun. (liens en double car match aller et retour)
def associationsList(dictRel):
	listlist = []
	for clef, valeurs in iter(dictRel.items()):
		for valeur in valeurs:
			for clef2, valeurs2 in iter(dictRel.items()):
				if (valeur in valeurs2 and clef2 != clef):
					listlist.append([clef, clef2])
	return listlist


def creer_fichier_rel(listlist):
	output = {}
#première boucle pour créer un dictionnaire avec une clef string "duo" qui correspond à une paire de fiches associées. La valeur liée à chaque clef est la pondération de cette association (en fonction du nombre de lien identique). Le duo_inverse sert à supprimer la moitié des relations, car elles sont créées dans les 2 sens par associationsList
#	with open('keywords/relations_ponderees.csv', 'w', encoding = 'utf8') as relfile:
#		spamwriter = csv.writer(relfile, delimiter='@', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	with open('keywords/relations_ponderees.csv', 'w', encoding = 'utf8') as relfile:
		for duo in listlist:
			duo_normal = duo[0] + '@' + duo[1]
			duo_inverse = duo[1] + '@' + duo[0]
			if ((duo_normal not in output) and (duo_inverse not in output)):
				ponderation = 0
				for duo2 in listlist:
					if duo2 == duo:
						ponderation += 1
						duokey = duo[0] + '@' + duo[1]
				output[duokey] = ponderation
				relfile.write(duokey + '@' + str(ponderation) + '\n')
		


dossier_des_keyfiches = 'keywords' #dossier contenant les fiches de mot clef normalisées (en .key)
dictionnaire_des_motclefs = create_dict_Keyword(dossier_des_keyfiches)
listetemp = associationsList(dictionnaire_des_motclefs)
creer_fichier_rel(listetemp)


