import pandas as pd
from collections import defaultdict
from typing import Union
from collections import Counter


def get_pos_data(data: pd.DataFrame) -> pd.DataFrame:
    return data[data.score >= 3]


def get_neg_data(data: pd.DataFrame) -> pd.DataFrame:
    return data[data.score < 3]


def filter_token(data, stopwords) -> list:
    reviews = data['tokenized'].str.replace(" ", "_")
    join_reviews = '_'.join(reviews)
    processed = join_reviews.split("_")
    filtered = [token for token in processed if token not in stopwords]
    return filtered


def filter_data(data: pd.DataFrame, since: Union[str, None], until: Union[str, None], area: str,
                place: list) -> pd.DataFrame:
    if place is not None: data = data[data['place'].isin(place)]
    if since is not None and until is not None: data.query('{} <= date <= {}'.format(since, until))
    if area is not None: data = data[data['area'] == area]
    return data


# area 별 관광지 추출
def extract_tour_area(data: pd.DataFrame) -> dict:
    result = defaultdict(list)
    tour_area = set([tuple(i) for i in data[['area', 'place']].values.tolist()])
    for item in tour_area:
        result[item[0]].append(item[1])
    return result


# 형태소 별 단어 리스트
def get_words_by_morph(data: pd.DataFrame, stopwords: list) -> dict:
    words_by_morph = defaultdict(list)
    token_list = filter_token(data, stopwords)
    for token in token_list:
        token_split = token.split("/")
        words_by_morph[token_split[1]].append(token_split[0])

    return {'명사': words_by_morph['NNG'] + words_by_morph['NNP'],
            '동사': words_by_morph['VV'],
            '형용사': words_by_morph['VA'],
            '어근': words_by_morph['XR'],
            '부정지정사': words_by_morph['VCN'] + words_by_morph['VX'] + words_by_morph['MAG']}


# 전체 데이터에서 출현 빈도 상위 단어 분포
def distribution_of_top_n_word(data: pd.DataFrame, stopwords: list, n: int) -> list:
    top_words = []

    tokens = filter_token(data, stopwords)
    counter = Counter(tokens)
    for word, count in counter.most_common(n):
        if word.split("/")[-1] in ['VA', 'VV']:
            word = word.replace('/', '다/')
        top_words.append({"word": word, "count": count})

    return top_words


# 형태소 별 데이터에서 출현 빈도 상위 단어 분포
def distribution_of_top_n_word_by_morph(data: pd.DataFrame, stopwords: list, n: int) -> dict:
    top_words_by_morph = {}

    for morph, words in get_words_by_morph(data, stopwords).items():
        top_words = Counter(words).most_common(n)
        if morph in ["동사", "형용사"]:
            top_words_by_morph[morph] = [{"word": word + "다", "count": count} for word, count in top_words]
            continue
        top_words_by_morph[morph] = [{"word": word, "count": count} for word, count in top_words]

    return top_words_by_morph


# 극성 별 데이터에서 출현 빈도 상위 단어 분포
def distribution_of_top_n_word_by_polarity(data: pd.DataFrame, stopwords: list, n: int) -> dict:
    n = 5
    pos = get_pos_data(data)
    neg = get_neg_data(data)

    result = {
        '긍정': distribution_of_top_n_word(pos, stopwords, n),
        '부정': distribution_of_top_n_word(neg, stopwords, n)
    }

    return result


# 평점 분포
def distribution_rating(data: pd.DataFrame) -> dict:
    scores = sorted(data.score.unique())
    nums = [len(data[data.score == s]) for s in scores]
    result = dict(zip(map(str, scores), nums))
    return result


# 극성(긍부정) 분포
def distribution_polarity(data: pd.DataFrame) -> dict:
    pos = get_pos_data(data)
    neg = get_neg_data(data)
    return {"긍정": len(pos), "부정": len(neg)}

