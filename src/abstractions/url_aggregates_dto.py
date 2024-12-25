from pydantic import BaseModel


class UrlAggregateDto(BaseModel):
    Id: str
    Url: str
    ShortUrl: str

    @staticmethod
    def create_from_domain(url_aggregate, basic_url, basic_prefix):
        result_dto = UrlAggregateDto(
            Id = url_aggregate.Id,
            Url = url_aggregate.Url,
            ShortUrl = url_aggregate.get_short_url(basic_url, basic_prefix)
        )

        return result_dto