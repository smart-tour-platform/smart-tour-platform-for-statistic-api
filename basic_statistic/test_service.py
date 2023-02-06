from unittest import TestCase
import service
from model.BasicStatistic import BasicStatistic
from collections import Counter, defaultdict
import re

path = "model/data/{}"
model = BasicStatistic(path)


class Test(TestCase):
    def test_tokenize(self):
        reviews = model.get_data()['tokenized'].str.replace(" ", "_")
        join_reviews = '_'.join(reviews)
        words = [review.split("/") for review in join_reviews.split("_")]
        for word in words:
            self.assertTrue(len(word) == 2)

    def test_filter_data(self):
        data = model.get_data()
        filter_data = service.filter_data(data, since=None, until=None, area="중구", place=["40계단 문화관"])
        self.assertTrue(len(data) != len(filter_data))

    def test_get_morph(self):
        # 형태소 별 단어 리스트
        morph = service.get_words_by_morph(model.get_data(), model.get_stopwords())
        self.assertTrue(len(morph.get("명사")) > 0)

    def test_distribution_rating(self):
        # 평점 분포
        data = model.get_data()
        scores = sorted(data.score.unique())
        nums = [len(data[data.score == s]) for s in scores]
        result = dict(zip(map(str, scores), nums))
        self.assertEqual(sum(result.values()), len(data))

    def test_distribution_of_polarity(self):
        # 평점 분포
        data = model.get_data()
        pos = service.get_pos_data(data)
        neg = service.get_neg_data(data)
        result = dict(zip(['긍정', '부정'], [len(pos), len(neg)]))
        self.assertEqual(sum(result.values()), len(data))

    def test_distribution_of_morph(self):
        # 주요 형태소(명사, 동사, 형용사, 어근, 부정 지정사) 분포
        data = model.get_data()
        morphs = service.get_words_by_morph(data, model.get_stopwords())
        result = {morph: len(words) for morph, words in morphs.items()}
        for value in morphs.values():
            for item in value:
                self.assertNotEqual(re.match("[가-힣]+", item), None)
        for key in result:
            self.assertEqual(type(result[key]), int)

    def test_distribution_of_top_n_word(self):
        # 전체 데이터에서 출현 빈도 상위 단어 추출
        data = model.get_data()
        n = 5
        tokens = service.filter_token(data, model.get_stopwords())

        counter = Counter(tokens)

        top_words = []

        for word, count in counter.most_common(n):
            if word.split("/")[-1] in ['VA', 'VV']:
                word = word.replace('/', '다/')
            top_words.append({"word": word, "count": count})

        for item in top_words:
            self.assertIn("/", item["word"])
            self.assertEqual(type(item["count"]), int)

    def test_distribution_of_top_n_word_by_morph(self):
        data = model.get_data()
        n = 5
        top_words_by_morph = {}

        for morph, words in service.get_words_by_morph(data, model.get_stopwords()).items():
            top_words = Counter(words).most_common(n)
            if morph in ["동사", "형용사"]:
                top_words_by_morph[morph] = [{"word": word + "다", "count": count} for word, count in top_words]
                continue
            top_words_by_morph[morph] = [{"word": word, "count": count} for word, count in top_words]

        self.assertEqual(list(top_words_by_morph.keys()), ["명사", "동사", "형용사", "어근", "부정지정사"])

        for value in top_words_by_morph.values():
            for item in value:
                self.assertNotIn("/", item["word"])
                self.assertEqual(type(item["count"]), int)

    def test_distribution_of_top_n_word_by_polarity(self):
        data = model.get_data()
        n = 5
        pos = service.get_pos_data(data)
        neg = service.get_neg_data(data)

        result = [
            {'긍정': service.distribution_of_top_n_word(pos, model.get_stopwords(), n)},
            {'부정': service.distribution_of_top_n_word(neg, model.get_stopwords(), n)}
        ]

        print(result)
