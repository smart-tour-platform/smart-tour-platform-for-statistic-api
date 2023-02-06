import pandas as pd
from typing import Union


def filter_data(data: pd.DataFrame, since: Union[str, None], until: Union[str, None], area: str,
                place: list) -> pd.DataFrame:
    if place is not None: data = data[data['place'].isin(place)]
    if since is not None and until is not None: data.query('{} <= date <= {}'.format(since, until))
    if area is not None: data = data[data['area'] == area]
    return data


def match(data: pd.DataFrame, dictionary: dict) -> list:
    tokens = ' '.join(data['token'].values.tolist())
    result = []
    for category, words in dictionary.items():
        review = tokens
        count = {"pos": 0, "neg": 0}
        for word, pol in words:
            review_count = review.count(word)
            if review_count == 0: continue
            if pol == 1: count["pos"] += review_count
            elif pol == -1: count["neg"] += review_count
            review = " ".join(review.split(word))
        result.append({"category": category, "count": count})
    return result
