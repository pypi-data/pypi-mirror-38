
import requests
from prometheus_client.core import GaugeMetricFamily

from exportme.exporters import Collector


class VersionOne(Collector):
    def get(self, url):
        response = requests.get(url.format(self.view.apikey))
        response.raise_for_status()
        return response.json()

    def collect(self):
        data = self.get('https://www.wanikani.com/api/user/{}/study-queue')
        yield GaugeMetricFamily('wanikani_level', 'Level', value=data['user_information']['level'])
        yield GaugeMetricFamily('wanikani_lessons', 'Level', value=data['requested_information']['lessons_available'])
        yield GaugeMetricFamily('wanikani_reviews', 'Level', value=data['requested_information']['reviews_available'])

        data = self.get('https://www.wanikani.com/api/user/{}/srs-distribution')
        levels = GaugeMetricFamily('wanikani_items', 'Levels of current items', labels=['level', 'item'])
        for level, items in data['requested_information'].items():
            for item, count in items.items():
                levels.add_metric([item, level], count)
        yield levels
