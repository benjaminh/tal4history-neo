#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import listdir
from os.path import isfile, join
from py2neo import Graph, Node, Relationship
from Fiche import Fiche

def analyseRelations(nom_fichier, dossier, graph):
    with open(join(dossier, nom_fichier)) as f:
        content = f.readlines()
        content = [x.strip('\n') for x in content]
        for line in content:
            fiche_id,fiche_liee_id,ponderation = line.split('@')    
            creationLiens(fiche_id.strip('fiche').strip('.txt'),fiche_liee_id.strip('fiche').strip('.txt'),ponderation,graph)
            
def creationLiens(fiche_id,fiche_liee_id,poids,graph):
    # Récupérer les noeuds du graphe correspondant aux fiches à lier
    node1 = graph.find_one('Fiche_descriptive', property_key='doc_position', property_value=fiche_id)
    node2 = graph.find_one('Fiche_descriptive', property_key='doc_position', property_value=fiche_liee_id)
    #Créer la relation correspondantes
    rel = Relationship.cast(node1, ("correle_a", {"complement": '',"ponderation": poids}), node2)
    # Créer le lien dans neo4j
    graph.create(rel)
    
  
def main(dossier, ignore_files):
    graph_db = Graph()

    # Pour chaque fiche de mots-clés, analyser son contenu
    # et créer les liens correspondants par cooccurrence de mot-clés
    # avec les autres fiches
    analyseRelations(fichier_relations,dossier,graph_db)

if __name__ == "__main__":
    dossier = "keywords"
    fichier_relations = "relations_ponderees.csv"    
    ignore_files = []
    main(dossier, ignore_files)
