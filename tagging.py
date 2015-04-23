#!/usr/bin/env python3
# encoding: utf-8

import os
import re
import glob
import csv

#regex
RligneSansContenu = re.compile(r'(Références associées:|titre:|fiche n°|auteur:|date:)', re.UNICODE)


#fonction pour construire une liste de mot-clef à partir d'un fichier .csv de mots clef 
#rentre tous les mots clefs sans tenir compte des synonymes
def load_keywordList(keyword_file_path):
	keywords = []
	with open(keyword_file_path, 'rt', encoding='utf8') as keywordFile:
		Keyfile = csv.reader(keywordFile, delimiter='\t', quotechar='"')
		for row in Keyfile:
			for key in row:
				keywords.append(key)
	return keywords

#construire un pattern regex de tous les mots clefs à partir d'une liste de mots-clefs (c'est le role de la fonction load_keywordList)
def build_keyword_regex(keyword_file_path):
	keyword_list = load_keywordList(keyword_file_path)
	keyword_regex_list = []
	for word in keyword_list:
		if word != '':
			word_regex = '\\b' + re.escape(word)				#version flexible permettant de prendre en compte les variation en fin de mot-clef (un "s" par exemple) produisant des match stables
	#		word_regex = '\\b' + re.escape(word) + '\\b'		#version permettant de rendre les mot-clefs invariants (exige un espace après)
			keyword_regex_list.append(word_regex)
	a = '|'.join(keyword_regex_list)
	keyword_pattern = re.compile(a, re.IGNORECASE)
	return keyword_pattern

#pour chaque fiche.xxx.txt , cette fonction crée un fiche.xxx.key qui contient les mots clefs de la fiche tels que trouvé dans le texte (non normalisé)
def create_keyword_fiche(uneFiche, keyword_pattern):
	with open(uneFiche, 'r', encoding = 'utf8') as Lafiche:
		ficheName = re.sub(r'fiches/', 'keywords/nonNormalised/', uneFiche) #enlève le chemin vers le dossier fiches/ pour la remplacer par le chemin vers le dossier /keywords
		KeywordsFiche = re.sub(r'.txt', '.key', ficheName) #enlève l'extension pour la remplacer par l'extension .key
		with open(KeywordsFiche, 'w', encoding = 'utf8') as KeyFiche:
			text = Lafiche.readlines()
			keywordFiche = []
			for line in text:
				if not re.match(RligneSansContenu, line):
					keywordLigne = re.findall(keyword_pattern, line)
					if keywordLigne != []:
						keywordFiche = keywordFiche + keywordLigne
			keywordFiche = list(map(str.lower, keywordFiche))
			keywordFiche = set(keywordFiche)
			if keywordFiche != []:
				for keyword in keywordFiche:
					KeyFiche.write(keyword + '\n')
			else:
				print(KeywordsFiche)

#pour chaque fiche .key créée par la fonction "create_keyword_fiche", cette fonction re-crée une fiche .key en remplaçant les mots clefs synonymes par leur valeur de base (valeur de base contenue dans la 1ere colone du csv)
def normalise_keyword(keyword_file_path):
	with open(keyword_file_path, 'rt', encoding = 'utf8') as keywordFile:
		keyfile = csv.reader(keywordFile, delimiter='\t', quotechar='"')
		mydict = {rows[0].lower():list(map(str.lower, rows[0:])) for rows in keyfile if rows[0] != ''} #gestion des synonymes: crer un dictionnaire avec pour clée le premier mot clef de la ligne du fichier csv, et avec pour valeurs tous les mots clefs de la ligne. Si la ligne ne commence pas par une case vide. 
		listFichesKey = glob.glob("keywords/nonNormalised/*.key")
		for fichekey in listFichesKey: 
			with open(fichekey, 'r', encoding = 'utf8') as lafichekey: #ouvre tour à tour chacune des ficheskey dans le dossier keywords/nonNormalised/
				ficheKeynormName = re.sub(r'nonNormalised/', '', fichekey) #modifie le chemin pour se placer dans keywords/ (et pas dans keywords/nonNormalised/)
				with open(ficheKeynormName, 'w', encoding = 'utf8') as KeyFichenorm: #créer une fiche dans keywords pour écrire les mots clefs normalisés
					keystags = lafichekey.readlines()
					keystags = list(map(lambda s: re.sub(r'\n', '', s), keystags)) #créer une list à partir du fichier 
					for keystag in keystags:
						keynorm = [key for key, value in iter(mydict.items()) if keystag in value] # remplace les valeurs par la clée correspondante à partir du dictionnaire élaboré précédement
						KeyFichenorm.write(keynorm[0] + '\n')

chemin_keywordfile = 'memoireMQkey.csv' #.csv de mots clef, avec les synonymes sur la même ligne
motsclefs = build_keyword_regex(chemin_keywordfile)

listFiches = glob.glob("fiches/*.txt")
for fiche in listFiches:
	if 'fiche' in fiche: #check si le mot fiche apparait dans le nom du fichier pour ne pas prendre en compte les fichier 'images' et 'références'
		create_keyword_fiche(fiche, motsclefs)
normalise_keyword(chemin_keywordfile)

