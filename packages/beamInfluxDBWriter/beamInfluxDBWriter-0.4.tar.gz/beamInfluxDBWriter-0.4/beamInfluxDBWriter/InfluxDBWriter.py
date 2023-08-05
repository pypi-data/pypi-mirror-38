from apache_beam.io import iobase
from influxdb import InfluxDBClient


class InfluxDBWriter(iobase.Writer):

    def __init__(self, client):
        self._client = client

    def write(self, value):
        self._client.write_points(value)

    def close(self):
        pass