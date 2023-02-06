import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path.format("data.csv"))
    df = df[df.language == '한국어'][['area', 'place', 'type', 'date', 'score', 'review', 'tokenized']]
    return df


def load_stopwords(path: str) -> list:
    df = pd.read_csv(path.format("stopwords.csv"))
    return df.stopword.tolist()


class BasicStatistic:
    def __init__(self, path: str):
        self.morph = ['NNP', 'NNG', 'VV', 'VA', 'XR', 'VCN']
        self.data = load_data(path)
        self.stopwords = load_stopwords(path)

    def get_data(self) -> pd.DataFrame:
        return self.data

    def get_stopwords(self) -> list:
        return self.stopwords

    def get_morph(self) -> list:
        return self.morph


