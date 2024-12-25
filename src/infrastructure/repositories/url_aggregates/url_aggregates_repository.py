import sqlite3
from datetime import datetime
from enum import Enum

from domain.url_aggregates import UrlAggregate


class CommonRepositoryAnswers(str, Enum):
    done = "done"
    optimistic_concurrency = "optimistic_concurrency"

class UrlAggregatesRepository:
    def __init__(self):
        self.db_tasks: [] = []
        self.db_root = "../app/data/data.db"
        self.table_name = "url_aggregates"
        self.migrate()


    def migrate(self):
        con = sqlite3.connect(self.db_root)
        cur = con.cursor()

        table_check_result = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

        tables_exist = table_check_result.fetchall()

        for table in tables_exist:
            if table[0] == self.table_name:
                return

        cur.execute(
            "CREATE TABLE url_aggregates(url UNIQUE, id, created_at, updated_at);"
        )

    def get_by_id(self, id):
        con = sqlite3.connect(self.db_root)
        cur = con.cursor()

        get_result = cur.execute("SELECT * FROM url_aggregates WHERE id = ?", (id,))

        if get_result.rowcount == 0:
            return None

        url_aggregate_db = get_result.fetchone()

        if url_aggregate_db is None:
            return None

        url_aggregate = UrlAggregate.create_from_db(
            url=url_aggregate_db[0],
            id=url_aggregate_db[1],
            created_at=datetime.fromisoformat(url_aggregate_db[2]),
            updated_at=datetime.fromisoformat(url_aggregate_db[3]),
        )

        return url_aggregate

    def get_by_url(self, url):
        con = sqlite3.connect(self.db_root)
        cur = con.cursor()

        get_result = cur.execute("SELECT * FROM url_aggregates WHERE url = ?", (url,))

        if get_result.rowcount == 0:
            return None

        url_aggregate_db = get_result.fetchone()

        url_aggregate = UrlAggregate.create_from_db(
            url=url_aggregate_db[0],
            id=url_aggregate_db[1],
            created_at=datetime.fromisoformat(url_aggregate_db[2]),
            updated_at=datetime.fromisoformat(url_aggregate_db[3]),
        )

        return url_aggregate

    def upsert(self, task_updated):
        con = sqlite3.connect(self.db_root)
        cur = con.cursor()

        upsert_result = cur.execute(
            "INSERT INTO url_aggregates(url, id, created_at, updated_at)" +
            " VALUES(" +
                    "'" + task_updated.Url + "',"
                    "'" + task_updated.Id + "',"
                    "'" + task_updated.CreatedAt.isoformat() + "',"
                    "'" + task_updated.UpdatedAt.isoformat() + "')"
            " ON CONFLICT(url) DO NOTHING")

        con.commit()
        return CommonRepositoryAnswers.done
