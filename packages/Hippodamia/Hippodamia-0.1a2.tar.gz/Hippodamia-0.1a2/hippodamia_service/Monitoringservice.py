from pelops.abstractmicroservice import AbstractMicroservice
import hippodamia_service


class Monitoringservice(AbstractMicroservice):
    _version = hippodamia_service.version

    def __init__(self, config, mqtt_client=None, logger=None):
        """
        Constructor - creates the services and the tasks

        :param config: config yaml structure
        :param mqtt_client: mqtt client instance
        :param logger: logger instance
        """
        AbstractMicroservice.__init__(self, config, "publish-gateway", mqtt_client, logger)

    def _start(self):
        raise NotImplementedError

    def _stop(self):
        raise NotImplementedError

    @classmethod
    def _get_description(cls):
        raise NotImplementedError

    @classmethod
    def _get_schema(cls):
        raise NotImplementedError


def standalone():
    Monitoringservice.standalone()


if __name__ == "__main__":
    Monitoringservice.standalone()
