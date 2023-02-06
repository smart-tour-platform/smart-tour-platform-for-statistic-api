from unittest import TestCase
from model.DictionarySentimental import DictionarySentimental
import service


model = DictionarySentimental("model/data/{}")


class Test(TestCase):
    def test_match(self):
        result = service.match(model.get_data(), model.get_dictionary())
        print(result)