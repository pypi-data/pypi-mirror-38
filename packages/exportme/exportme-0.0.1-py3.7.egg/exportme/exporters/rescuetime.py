import requests
from prometheus_client.core import GaugeMetricFamily

from exportme.exporters import Collector


class RescueTime(Collector):
    def collect(self):
        response = requests.get('https://www.rescuetime.com/anapi/daily_summary_feed', params={
            'key': self.view.apikey,
        })

        response.raise_for_status()
        data = response.json()[0]

        yield GaugeMetricFamily('rescutime_pulse', 'Productivity Pulse', value=data['productivity_pulse'])
        yield GaugeMetricFamily('rescuetime_uncatagorized', 'Unknown', value=data['uncategorized_hours'] * 60)
