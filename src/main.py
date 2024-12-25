from datetime import datetime

import uvicorn
import os
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from starlette.responses import RedirectResponse

from common.error import ValidationErrorResponse, NotFoundErrorResponse
from infrastructure.repositories.url_aggregates.url_aggregates_repository import CommonRepositoryAnswers, UrlAggregatesRepository
from common.error import OptimisticConcurrencyErrorResponse
from abstractions.url_aggregates_dto import UrlAggregateDto
from domain.url_aggregates import UrlAggregate

app = FastAPI()

basic_url = os.environ.get('BASIC_URl', "localhost:8008")
basic_prefix = os.environ.get('BASIC_PREFIX', "http://")

url_repository = UrlAggregatesRepository()

@app.get('/')
def root():
    data = "root"
    return PlainTextResponse(content=data, status_code = 200)

@app.get('/s/{id}')
def get_redirection_to_short_url(id:str):
    url_aggregate = url_repository.get_by_id(id)

    if url_aggregate is None:
        response = NotFoundErrorResponse("Short url does not exist for id '" + id + "'")
        return response

    return RedirectResponse(
        url=url_aggregate.Url, status_code = 302
    )


@app.get('/url_aggregate')
def get_url_aggregate_by_url(url:str):

    url_aggregate = url_repository.get_by_url(url)

    if url_aggregate is None:
        response = NotFoundErrorResponse("Short url does not exist for url '" + url + "'")
        return response

    url_aggregate_dto = UrlAggregateDto.create_from_domain(url_aggregate, basic_url, basic_prefix)

    json_data = jsonable_encoder(url_aggregate_dto)

    return JSONResponse(content=json_data, status_code = 200)

@app.post('/url_aggregate')
def add_url_aggregate(url:str):

    new_url_aggregate = UrlAggregate.create_new(
        url=url,
    )

    result = url_repository.upsert(new_url_aggregate)

    if result == CommonRepositoryAnswers.optimistic_concurrency:
        return OptimisticConcurrencyErrorResponse()

    url_aggregate_dto = UrlAggregateDto.create_from_domain(new_url_aggregate, basic_url, basic_prefix)
    json_data = jsonable_encoder(url_aggregate_dto)

    return JSONResponse(content=json_data, status_code = 200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)