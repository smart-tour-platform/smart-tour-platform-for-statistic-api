from unittest import TestCase
import service


class Test(TestCase):
    def test_predict(self):
        result = service.predict("기장축제 멸치 맛있어요.")
        print(result)
