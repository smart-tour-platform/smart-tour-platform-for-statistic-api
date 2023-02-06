from fastapi import APIRouter
from pydantic import BaseModel
from typing import Union
from dictionary_sentimental.model.DictionarySentimental import DictionarySentimental
import dictionary_sentimental.service as service


class ParameterRequest(BaseModel):
    since: Union[str, None] = None
    until: Union[str, None] = None
    area: Union[str, None] = None
    place: Union[list, None] = None


router = APIRouter()
path = "dictionary_sentimental/model/data/{}"
model = DictionarySentimental(path)


def get_data(params):
    data = model.get_data()
    if params is not None: data = service.filter_data(
        data, params.since, params.until, params.area, params.place)
    return data


@router.get(
    "/api/dictionary/sentimental",
    summary="사전 기반 감성 분석"
)
def dictionary_sentimental(params: Union[ParameterRequest, None] = None):
    data = get_data(params)
    return {"data": service.match(data, model.get_dictionary())}
