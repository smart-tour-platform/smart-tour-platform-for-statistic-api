from fastapi import APIRouter
from pydantic import BaseModel
from basic_statistic import service
from basic_statistic.model.BasicStatistic import BasicStatistic
from typing import Union


class ParameterRequest(BaseModel):
    since: Union[str, None] = None
    until: Union[str, None] = None
    area: Union[str, None] = None
    place: Union[list, None] = None


router = APIRouter()
data_path = "basic_statistic/model/data/{}"
model = BasicStatistic(data_path)


@router.get("/api/basic/test")
def test():
    return {"test": "test"}


def get_data(params):
    data = model.get_data()
    if params is not None: data = service.filter_data(
        data, params.since, params.until, params.area, params.place)
    return data


@router.get(
    "/api/basic/extract/area",
    summary="지역 목록 추출"
)
def extract_area(params: Union[ParameterRequest, None] = None):
    data = get_data(params)
    return {"data": service.extract_tour_area(data)}


@router.get(
    "/api/basic/distribution/rate",
    summary="평점 분포"
)
def distribution_by_rate(params: Union[ParameterRequest, None] = None):
    data = get_data(params)
    return {"data": service.distribution_rating(data)}


@router.get(
    "/api/basic/distribution/morph",
    summary="형태소 별 분포"
)
def distribution_by_morph(params: Union[ParameterRequest, None] = None):
    data = get_data(params)
    return {"data": service.distribution_polarity(data)}


@router.get(
    "/api/basic/distribution/top-word",
    summary="상위 단어 추출"
)
def distribution_top_word(n: Union[int, None] = 30, params: Union[ParameterRequest, None] = None):
    """
    상위 단어 추출, 기본값 30
    :param n: 상위 몇 개의 단어를 추출할 것인지
    :param params: data 필터링 조건
    :return:
    """
    data = get_data(params)
    return {"data": service.distribution_of_top_n_word(data, model.get_stopwords(), n)}


@router.get(
    "/api/basic/distribution/top-word/morph",
    summary="형태소 별 상위 단어 추출"
)
def distribution_top_word_by_morph(n: Union[int, None] = 30, params: Union[ParameterRequest, None] = None):
    """
    형태소 별 상위 단어 추출, 기본값 30
    :param n: 상위 몇 개의 단어를 추출할 것인지
    :param params:
    :return:
    """
    data = get_data(params)
    return {"data": service.distribution_of_top_n_word_by_morph(data, model.get_stopwords(), n)}


@router.get(
    "/api/basic/distribution/top-word/polarity",
    summary="평점 별 상위 단어 추출"
)
def distribution_top_word_by_polarity(n: Union[int, None] = 30, params: Union[ParameterRequest, None] = None):
    """
    평점 별 상위 단어 추출, 기본값 30
    :param n: 상위 몇 개의 단어를 추출할 것인지
    :param params:
    :return:
    """
    data = get_data(params)
    return {"data": service.distribution_of_top_n_word_by_polarity(data, model.get_stopwords(), n)}