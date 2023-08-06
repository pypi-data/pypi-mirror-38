import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.abstractmicroservice import AbstractMicroservice
from hippodamia_agent.monitoringagent import MonitoringAgent


class TestService(AbstractMicroservice):
    _version = 0.1
    _monitoring_agent = None

    def __init__(self, config, mqtt_client=None, logger=None):
        """
        Constructor - creates the services and the tasks

        :param config: config yaml structure
        :param mqtt_client: mqtt client instance
        :param logger: logger instance
        """
        AbstractMicroservice.__init__(self, config, "testservice", mqtt_client, logger)
        self._monitoring_agent = MonitoringAgent(config, self, self._mqtt_client, self._logger)

    def _handler(self, message):
        self._logger.info("received messages - publishing message")
        self._mqtt_client.publish("/test/service/pub", message)

    def _start(self):
        self._mqtt_client.subscribe("/test/service/sub", self._handler)
        self._monitoring_agent.start()

    def _stop(self):
        self._mqtt_client.unsubscribe("/test/service/sub", self._handler)
        self._monitoring_agent.stop()

    @classmethod
    def _get_description(cls):
        return "test service for hippodamia"

    @classmethod
    def _get_schema(cls):
        return {
            "testservice": {
            }
        }


def standalone():
    TestService.standalone()


if __name__ == "__main__":
    TestService.standalone()
