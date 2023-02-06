from unittest import TestCase
from model.SemanticSearch import SemanticSearch
import service

model = SemanticSearch(lang="한국어", path="model/data/{}")


class Test(TestCase):
    def test_semantic_search(self):
        data = model.get_data()
        embedded = model.get_embedded()
        embedder = model.get_embedder()

        rank = service.get_rank(data=data, embedder=embedder, embedded=embedded, query="야경이 아름답다.", threshold=0.5)
        self.assertIsNotNone(rank)

