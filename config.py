from pydantic import BaseSettings


class AppConfig(BaseSettings):
    oncall_url: str
    scrape_interval: int = 10