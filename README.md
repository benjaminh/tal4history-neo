# tal4history-neo
Script Python pour l'indexation semi-automatique de données historiques dans Neo4j.

Auteurs:
- Matthieu Quantin
- Benjamin Hervy

# Mise en place
## Créer les dossiers suivants en respectant l'arborescence
- BeingClean
- keywords
- keywords/nonNormalised
- fiches

## Ordre d'exécution des opérations
- Latex2Fiche.py (appelle CleanLaTeX.py et Fichage.py) : créer les fiches à partir d'un fichier LaTeX simple.
- txt2neo.py (appelle fiche.py et source.py) : créer les noeuds correspondant aux fiches dans une BDD Neo4j. De même pour les sources et les liens entre sources et fiches.
- tagging.py : pour chaque fiche xxxx.txt créer une fiche xxxx.key de mots-clef associés
- key2relation.py : à partir des fiches xxxx.key, créer un fichier d'association de fiches sans doublons et avec pondération.
- relation2neo.py : à partir du fichier d'association, générer les liens correspondant dans Neo4j.

## Améliorations futures

* Fichage.py : Images non prises en compte par l'add-on Writer2latex. Ces images sont correctement extraites mais la ligne \includegraphics est commentée dans le LaTeX
* Fichage.py : Gestion des `itemize`. Il sont pour l'instant gérés comme de simple lignes de texte... idée à trouver... 
* Gestion des liens entre fiches: plutôt que d'avoir des pondérations globales sur des liens indifférenciés; 2 options d'amélioration: 
	- Ajouter la liste des mots-clef commun entre 2 fiches dans les propriétés du lien. Plus éventuellement la pondération de chacun des mots-clef. Problème: comment y accéder? 
	- Créer un lien pour chaque mot clef commun. Possibilité de pondération de ces liens. Exemple: la fiche `A` contient 5 occurrences du mot-clef `x` et la fiche `B` en contient 10; alors le lien typé `x` entre ces fiches est pondéré de 5²/10. Problème: création de beaucoup de liens.
