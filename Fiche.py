#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from py2neo import Graph, GraphError, Node, Relationship
from Source import Source


class Fiche(object):

    '''Modèle de noeud relatif aux fiches descriptives
    La classe possède deux méthodes pour créer des fiches
    et des relations entre fiches
    '''

    def __init__(self, node):
        self._node = node

    @classmethod
    def create_node(self, graph_db, tmp_id, titre, auteur,
                    contenu, date_creation):

        self.node_type = "Fiche_descriptive"

        # Ajouter propriétés du type "modified" ?
        fiche_properties = {'doc_position': tmp_id, 'titre': titre,
                            'auteur': auteur, 'contenu': contenu, 'date_creation': date_creation}
        fiche_node = Node.cast(fiche_properties)
        fiche_node.labels.add(self.node_type)
        graph_db.create(fiche_node)

        return Fiche(fiche_node)

    @classmethod
    def create_rel(self, graph_db, fiche_liee, complement):
        rel = Relationship.cast(self, ("correle_a",
                                {"complement": complement}), fiche_liee)
        graph_db.create(rel)
        
    @classmethod
    def create_rel_recit(self, graph_db, fiche_liee, complement):
        rel = Relationship.cast(self, ("recit_lineaire",
                                {"complement": complement}), fiche_liee)
        graph_db.create(rel)

    def create_doc(self, graph_db, source, complement):
        rel = Relationship.cast(source, ("documente",
                                {"complement": complement}), self)
        graph_db.create(rel)

    @property
    def titre(self):
        return self._node["titre"]
