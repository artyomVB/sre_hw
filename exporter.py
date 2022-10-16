import time

import requests
from config import AppConfig
from prometheus_client import start_http_server, Gauge


TOTAL_NUMBER_OF_TEAMS = Gauge("total_number_of_teams", "Total number of teams")
NUMBER_OF_TEAMS_WITHOUT_PRIMARY_OR_SECONDARY = Gauge("number_of_teams_without_primary_or_secondary", "Number of bad teams")


class Collector:
    def __init__(self, scrape_interval, target_api):
        self.scrape_interval = scrape_interval
        self.target_api = target_api

    def collect_metrics(self):
        while True:
            teams = requests.get(f"{self.target_api}/api/v0/teams")
            TOTAL_NUMBER_OF_TEAMS.set(len(teams.json()))
            counter = 0
            for team in teams.json():
                resp = requests.get(f"{self.target_api}/api/v0/teams/{team}/summary")
                current = resp.json()["current"]
                if not current.get("primary") or not current.get("secondary"):
                    counter += 1
            NUMBER_OF_TEAMS_WITHOUT_PRIMARY_OR_SECONDARY.set(counter)
            time.sleep(self.scrape_interval)


if __name__ == "__main__":
    start_http_server(8000)
    config = AppConfig()
    c = Collector(config.scrape_interval, config.oncall_url)
    c.collect_metrics()
