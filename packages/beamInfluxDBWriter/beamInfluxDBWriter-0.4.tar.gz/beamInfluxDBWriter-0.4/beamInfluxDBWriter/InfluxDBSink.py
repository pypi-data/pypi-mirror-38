from apache_beam.io import iobase
from influxdb import InfluxDBClient
import InfluxDBWriter

class InfluxDBSink(iobase.Sink):

    def __init__(self, host, port, username, password, dbname):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._dbname = dbname


    def initialize_write(self):
        client = InfluxDBClient(self._host, self._port, self._username, self._password, self._dbname)
        return client

    def open_writer(self, init_result, uid):
        return InfluxDBWriter.InfluxDBWriter(init_result)

    def pre_finalize(self, init_result, writer_results):
        pass

    def finalize_write(self, init_result, writer_results, pre_finalize_result):
        pass