#!/usr/bin/env python3
# encoding: utf-8

import os
import re

#LAST STEP

#RnamePict = re.compile(r'(?<=\\includegraphics{)(.*)(?=})', re.UNICODE) #recupère le nom de l'image (chemin dans son dossier) après suppression des para d'affichage (cf ci-dessus)
RcaptionPict = re.compile(r'(?<=\\caption{)([^}]*)(?=})', re.UNICODE) #recupère la légende de l'image
Rfootnote = re.compile(r'(\\footnote)([^}]*})', re.UNICODE) #récupere l'ensemble (la footnote) pour le supprimer
RcontenuFootnote = re.compile(r'(?<=\\footnote{)([^}]*)(?=})', re.UNICODE) # recupère le contenu de la footnote
RcontenuFootnotetext = re.compile(r'(?<=\\footnotetext{)([^}]*)(?=})', re.UNICODE) # recupère le contenu de la footnotetext
RnombreuxSauts = re.compile(r'((?<=\n)(\s+)(?=\S))', re.UNICODE) 
Picts = open('fiches/images.txt', 'w', encoding = 'utf8')
Refs = open('fiches/references.txt', 'w', encoding = 'utf8')
Rtitresection = re.compile(r'(?<=\\section{)(.*)(?=})', re.UNICODE) #récupere le contenu (le titre)
Rtitresubsection = re.compile(r'(?<=\\subsection{)(.*)(?=})', re.UNICODE) #récupere le contenu (le titre)
Rtitresubsubsection = re.compile(r'(?<=\\subsubsection{)(.*)(?=})', re.UNICODE) #récupere le contenu (le titre)
Rtitreparagraph = re.compile(r'(?<=\\paragraph{)(.*)(?=})', re.UNICODE) #récupere le contenu (le titre)


def EcrireSectionPrecedente(identifiant, taille, tailleMinimum, titreSection, ContenuTxtSection, identifiantsRefs):
	if taille > tailleMinimum:
		nomfichierFiche = 'fiches/fiche' + identifiant + '.txt'
		with open(nomfichierFiche, 'w', encoding = 'utf8') as fiche:
			fiche.write('fiche n° '+ identifiant +'\n')
			fiche.write('titre: ' + titreSection + '\n\n\n')
			contenujoin = '\n'.join(ContenuTxtSection)
			contenujoin = re.sub(RnombreuxSauts, "\n", contenujoin)
			contenujoin = re.sub(Rfootnote, "", contenujoin)
			fiche.write(contenujoin)
			fiche.write('\n\n\nRéférences associées: '+ str(identifiantsRefs)) #au cas où... 
			fiche.close()

def CompteurMots(uneligne):
	if uneligne[0] != '\n':
		motsLigne = uneligne.split()
		#motsLigne.append(" ") # pour ne pas avoir de motsLigne vide qui donne des erreur de len()
		nombre = len(motsLigne)
	else:
		nombre = 0
	return nombre

def Image(identifiant, thisline, nextline, RnamePict):
	PictName = re.findall(RnamePict, thisline)
	if "caption" in nextline:
		PictLegende = re.findall(RcaptionPict, nextline)
	else:
		PictLegende = ['Pas_de_legende']
	Picts.write(identifiant + '@' + PictName[0] + "\@" + PictLegende[0] + '\n')

def References(thisline, RefID):
	RefIDLigne = []
	linereferences = re.findall(RcontenuFootnote, thisline) # attention il peut y avoir plusieurs footnote par ligne
	linereferences += re.findall(RcontenuFootnotetext, thisline)
	for refere in linereferences:
		RefID += 1
		RefIDLigne.append(RefID)
		Refs.write(str(RefID) + '@' + refere + '\n')
	return RefIDLigne


def decoupe(OrigineFile, conclusion, tailleMini, step, decoupeParagraphe):
	OrigineFileName = re.sub('.tex', '', OrigineFile)
	extensionEtapePrec = '.Step' + str(step-1) + '.txt'
	FichierPropre = 'BeingClean/' + OrigineFileName + extensionEtapePrec

	DossierImage = re.sub('_', '', OrigineFileName)
	DossierImage = DossierImage + '-img/'
	RpictName = re.compile(r"(?<=\\includegraphics{" + re.escape(DossierImage) + r')(.*)(?=})', re.UNICODE)
	print ("(?<=\\includegraphics{" + re.escape(DossierImage) + r')(.*)(?=})')

	with open(FichierPropre, 'r', encoding = 'utf8') as fichierpropre:
		text = fichierpropre.readlines()

		titre = " " #pour amorcer
		RefIDsection = []
		contenutxt = []
		numref = 0
		i = 0
		sec = 0
		subsec = 0
		subsubsec = 0
		parag = 0
		NbMotsSect = 0

		for line in text:
			i += 1
			NbMotsSect += CompteurMots(line)
			if not decoupeParagraphe:
				IDf = str(sec) + "." + str(subsec) + "." + str(subsubsec)
			else:
				IDf = str(sec) + "." + str(subsec) + "." + str(subsubsec) + "." + str(parag)

			if "\includeg" in line:
				Image(IDf, line, text[i], RpictName) 

			if "\\footnote" in line:
				RefLigne = References(line, numref)
				RefIDsection += RefLigne
				numref += len(RefLigne)

			if not decoupeParagraphe:
				if "\paragraph" in line: 
					titreparagraphe = re.findall(Rtitreparagraph, line)
					titreparagraphe = "\n" + titreparagraphe[0]
					contenutxt.append(titreparagraphe)
			else:
				if "\paragraph" in line: 
					EcrireSectionPrecedente(IDf, NbMotsSect, tailleMini, titre, contenutxt, RefIDsection)
					contenutxt = []
					RefIDsection = []
					NbMotsSect = 0
					ti = re.findall(Rtitreparagraph, line)
					titre = ti[0]
					parag += 1


			if "\\" not in line[0]:
				contenutxt.append(line)

			if re.match(r'^\\footnote', line):
				contenutxt.append(line)

			if "\section" in line: 
				EcrireSectionPrecedente(IDf, NbMotsSect, tailleMini, titre, contenutxt, RefIDsection)
				contenutxt = []
				RefIDsection = []
				NbMotsSect = 0
				ti = re.findall(Rtitresection, line)
				titre = ti[0]
				sec += 1
				subsec = 0
				subsubsec = 0
				parag = 0

			if "\subsection" in line:
				EcrireSectionPrecedente(IDf, NbMotsSect, tailleMini, titre, contenutxt, RefIDsection)
				contenutxt = []
				RefIDsection = []
				NbMotsSect = 0
				ti = re.findall(Rtitresubsection, line)
				titre = ti[0]
				subsec += 1
				subsubsec = 0
				parag = 0

			if "\subsubsection" in line:
				EcrireSectionPrecedente(IDf, NbMotsSect, tailleMini, titre, contenutxt, RefIDsection)
				contenutxt = []
				RefIDsection = []
				NbMotsSect = 0
				ti = re.findall(Rtitresubsubsection, line)
				titre = ti[0]
				subsubsec += 1
				parag = 0

			if conclusion: 
				EcrireSectionPrecedente(IDf, NbMotsSect, tailleMini, titre, contenutxt, RefIDsection)




