# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Union
from fastapi import APIRouter
from semantic_search.model.SemanticSearch import SemanticSearch
from semantic_search import service


class ParameterRequest(BaseModel):
    since: Union[str, None] = None
    until: Union[str, None] = None
    area: Union[str, None] = None
    place: Union[list, None] = None
    query: str


router = APIRouter()
data_path = "semantic_search/model/data/{}"
model = SemanticSearch(path=data_path, lang="한국어")


def get_data(params):
    data = model.get_data()
    if params is not None: data = service.filter_data(
        data, params.since, params.until, params.area, params.place)
    return data


@router.post(
    "/api/search",
    summary="시맨틱 서치"
)
def semantic_search(params: Union[ParameterRequest, None] = None):
    """
    시맨틱 서치
    :param params: query = required
    :return:
    """
    data = get_data(params)
    embedded = model.get_embedded()
    embedder = model.get_embedder()
    return {"data": service.get_rank(
        data=data,
        embedded=embedded,
        embedder=embedder,
        query=params.query,
        threshold=0.5)}
