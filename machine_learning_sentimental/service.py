from machine_learning_sentimental.model.MultiClassificationModel import MultiClassificationModel

model = MultiClassificationModel()


def predict(query: str) -> dict:
    return model.predict(query=query)
