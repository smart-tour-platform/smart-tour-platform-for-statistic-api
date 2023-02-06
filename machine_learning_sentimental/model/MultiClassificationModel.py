import pandas as pd
import numpy as np
from tqdm.auto import tqdm
from transformers import BertTokenizerFast as BertTokenizer
from machine_learning_sentimental.model.ToxicCommentTagger import ToxicCommentTagger


def get_category():
    category = {
        1: '재미',
        2: '프로그램',
        3: '먹거리',
        4: '살거리',
        5: '사전홍보',
        6: '안내/해설',
        7: '지역문화',
        8: '안전',
        9: '접근성/주차장',
        10: '재방문/방문유도',
        11: '편의시설',
        12: '기타',
        13: '조경물/풍경',
        14: '날씨/기온',
        15: '인파/혼잡도'
    }
    category = dict(zip([i[1] for i in category.items()], category.keys()))
    return category


class MultiClassificationModel:
    def __init__(self):
        self.LABEL_COLUMNS = ['재미', '프로그램', '먹거리', '살거리', '사전홍보', '안내/해설', '지역문화', '안전', '접근성/주차장', '재방문/방문유도', '편의시설',
                              '기타', '조경물/풍경', '날씨/기온', '인파/혼잡도']
        self.tokenizer = BertTokenizer.from_pretrained('klue/bert-base', local_files_only=False)

        self.trained_model = ToxicCommentTagger.load_from_checkpoint(
            'machine_learning_sentimental/model/data/best-checkpoint.ckpt',
            n_classes=len(self.LABEL_COLUMNS)
        )
        self.trained_model.eval()
        self.trained_model.freeze()
        self.category = get_category()

    def predict(self, query: str) -> dict:
        encoding = self.tokenizer.encode_plus(
            query,
            add_special_tokens=True,
            max_length=512,
            return_token_type_ids=False,
            padding="max_length",
            return_attention_mask=True,
            return_tensors='pt',
        )
        _, test_prediction = self.trained_model(encoding["input_ids"], encoding["attention_mask"])
        test_prediction = test_prediction.flatten().numpy()
        result = dict()
        for label, prediction in zip(self.LABEL_COLUMNS, test_prediction):
            # print(f"{label}: {prediction}")
            result[label] = int(prediction * 100)
        return result
