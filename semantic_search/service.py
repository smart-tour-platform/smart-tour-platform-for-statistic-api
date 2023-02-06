import pandas as pd
from typing import Union
from sentence_transformers import SentenceTransformer, util
import torch
from collections import Counter


def filter_data(data: pd.DataFrame, since: Union[str, None], until: Union[str, None], area: str,
                place: list) -> pd.DataFrame:
    if place is not None: data = data[data['place'].isin(place)]
    if since is not None and until is not None: data.query('{} <= date <= {}'.format(since, until))
    if area is not None: data = data[data['area'] == area]
    return data


def filter_corpus_embedding(corpus: pd.DataFrame, embedding: 'Tensor') -> 'Tensor':
    index = corpus['key']
    result = [v for i, v in enumerate(embedding) if i in index]
    return torch.stack(result, dim=0)


def get_rank(data: pd.DataFrame, embedder: SentenceTransformer, embedded: 'Tensor', query: str,
             threshold: float) -> list:
    query_embedding = embedder.encode(query, convert_to_tensor=True)
    embedding_corpus = filter_corpus_embedding(data, embedded)

    cos_scores = util.pytorch_cos_sim(query_embedding, embedding_corpus)[0]
    top_results = torch.topk(cos_scores, k=len(cos_scores))

    places = data['place'].tolist()

    relevant_places = []
    for score, index in zip(top_results[0], top_results[1]):
        if score < threshold: break
        relevant_places.append(places[index])

    top_places = [{"place": item[0], "count": item[1]} for item in Counter(relevant_places).most_common()]

    return top_places
