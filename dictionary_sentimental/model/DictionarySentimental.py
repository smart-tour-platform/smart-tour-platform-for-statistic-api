import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path.format("data.csv"))
    return df[df.language == "한국어"]


def load_dictionary(path: str) -> dict:
    category = pd.read_csv(path.format("category.csv"))["name"].values.tolist()
    dictionary = pd.read_csv(path.format("dictionary.csv"))
    dictionary = dictionary.sort_values(by="word", key=lambda x: x.str.len(), ascending=False)
    words = [dictionary[dictionary.category == idx][["word", "pol"]].values.tolist()
             for idx in range(len(category))]
    return dict(zip(category, words))


class DictionarySentimental:
    def __init__(self, path: str):
        self.data = load_data(path)
        self.dictionary = load_dictionary(path)

    def get_data(self):
        return self.data

    def get_dictionary(self):
        return self.dictionary
