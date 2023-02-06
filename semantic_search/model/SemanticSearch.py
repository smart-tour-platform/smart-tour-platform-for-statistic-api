import pandas as pd
import torch
import numpy as np
from sentence_transformers import SentenceTransformer


def load_data(path: str) -> pd.DataFrame:
    data = pd.read_csv(path.format("data.csv"))
    return data


def load_embedding_data(path: str) -> 'Tensor':
    data = torch.from_numpy(np.load(path.format("embedding_data.npy")))
    return data.to('cuda') if torch.cuda.is_available() else data


def load_embedder(lang: str) -> SentenceTransformer:
    model_name = {'한국어': 'jhgan/ko-sbert-multitask',
                  '영어': 'all-mpnet-base-v2',
                  '일본어': 'colorfulscoop/sbert-base-ja',
                  '중국어': 'uer/sbert-base-chinese-nli'}
    return SentenceTransformer(model_name[lang])


class SemanticSearch:
    def __init__(self, lang: str, path: str):
        self.data = load_data(path)
        self.embedded = load_embedding_data(path)
        self.embedder = load_embedder(lang)

    def get_data(self):
        return self.data

    def get_embedded(self):
        return self.embedded

    def get_embedder(self):
        return self.embedder
