import requests
from prometheus_client.core import GaugeMetricFamily

from miscprom.core.util import Collector


class Currency(Collector):
    def collect(self):
        url = "https://openexchangerates.org/api/latest.json"
        result = requests.get(url, params={"app_id": self.view.apikey})
        result.raise_for_status()
        json = result.json()

        metric = GaugeMetricFamily(
            "currency_rate", "Currency Rate", labels=["source", "destination"]
        )
        metric.add_metric(["usd", "jpy"], json["rates"]["JPY"])
        metric.add_metric(["usd", "eur"], json["rates"]["EUR"])
        yield metric
