from datetime import datetime, timezone
import uuid
from pydantic import BaseModel
from enum import Enum
class UrlAggregate(BaseModel):
    Id: str
    Url: str
    CreatedAt: datetime
    UpdatedAt: datetime

    @staticmethod
    def create_new(
        url: str):

        new_id = str(uuid.uuid4())
        utc_now = datetime.now(timezone.utc)

        task = UrlAggregate(
            Id = new_id,
            Url = url,
            CreatedAt = utc_now,
            UpdatedAt = utc_now,
        )

        return task

    @staticmethod
    def create_from_db(
        id: str,
        url: str,
        created_at: datetime,
        updated_at: datetime,):

        task = UrlAggregate(
            Id = id,
            Url = url,
            CreatedAt = created_at,
            UpdatedAt = updated_at,
        )

        return task

    def get_short_url(self, basic_url, basic_prefix):
        url = basic_prefix + basic_url + "/s/" + self.Id
        return url