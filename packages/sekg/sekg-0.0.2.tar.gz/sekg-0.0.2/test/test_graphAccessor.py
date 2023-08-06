from unittest import TestCase

from py2neo import Node, Graph

from sekg.graph.accessor import GraphAccessor
from sekg.graph.factory import GraphInstanceFactory


class TestGraphAccessor(TestCase):
    def test_get_graph(self):
        factory = GraphInstanceFactory("config.json")
        graph = factory.create_py2neo_graph_by_server_id(1)
        accessor = GraphAccessor(graph=graph)
        self.assertTrue(isinstance(accessor.graph, Graph))

    def test_is_connect(self):
        factory = GraphInstanceFactory("config.json")
        graph = factory.create_py2neo_graph_by_server_id(1)
        accessor = GraphAccessor(graph=None)
        self.assertFalse(accessor.is_connect())
        accessor = GraphAccessor(graph=graph)
        self.assertTrue(accessor.is_connect())

    def test_get_id(self):
        self.fail()

    def test_merge_relation(self):
        self.fail()

    def test_merge_node(self):
        factory = GraphInstanceFactory("config.json")
        graph = factory.create_py2neo_graph_by_server_id(1)

        accessor = GraphAccessor(graph=graph)
        self.assertTrue(accessor.is_connect())

        node = Node("test", name="lmw", male=1)

        accessor.merge_node(node, "test", "name")
        print(node)
        self.assertTrue(accessor.is_remote(node))

        self.assertTrue(accessor.is_remote(node))
        graph.delete(node)

    def test_push_node(self):
        self.fail()

    def test_find_node_by_id(self):
        self.fail()

    def test_find_relation_by_id(self):
        self.fail()
