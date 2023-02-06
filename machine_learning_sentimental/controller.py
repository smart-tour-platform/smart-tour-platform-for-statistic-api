from fastapi import APIRouter
from typing import Union
from pydantic import BaseModel
from machine_learning_sentimental.model.MultiClassificationModel import MultiClassificationModel
import machine_learning_sentimental.service as service


class ParameterRequest(BaseModel):
    query: str


router = APIRouter()
model = MultiClassificationModel()


@router.post(
    "/api/ml/predict",
    summary="기계 학습 기반 감성 분석"
)
def predict(params: ParameterRequest):
    """
    기계 학습 기반 감성 분석, 데이터 필터링 필요 없음
    :param params: {"query": 문장}
    :return:
    """
    return {"data": service.predict(query=params.query)}
