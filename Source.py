#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from py2neo import Graph, GraphError, Node, Relationship


class Source(object):

    def __init__(self, node):
        self._node = node

    @classmethod
    def create_source(self, graph_db, type_source,
                      ref_source, filename, auteur, contenu):

        self.node_type = "Source"

        # Ajouter propriétés du type "modified" ?
        source_properties = {'ref_source': ref_source, 'auteur':
                             auteur, 'legende': contenu}
        source_node = Node.cast(fiche_properties)
        source_node.labels.add(self.node_type)
        source_node.labels.add(type_source)
        graph_db.create(source_node)

        return Source(source_node)

    @property
    def legende(self):
        return self._node["legende"]
