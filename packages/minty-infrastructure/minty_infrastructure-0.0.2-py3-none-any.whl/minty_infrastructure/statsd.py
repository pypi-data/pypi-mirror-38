import logging

from statsd import StatsClient


def statsd_from_config(config: dict) -> StatsClient:
    """Get initialized StatsClient from config.

    If 'statsd' entry can't be found in the config a mocked client will be
    returned

    :param config: should contain:
        `{'statsd:{
                {
                'host': 'statsd host',
                'port': 1234
                }
            }}`
    :type config: dict
    :return: statsd client
    :rtype: StatsClient or StatsdMock
    """
    try:
        client = StatsClient(**config["statsd"])
    except KeyError:
        client = StatsdMock()
    return client


class StatsdMock:
    """Mock of statsdClient to be used when initialization fails."""

    def __init__(self):
        """Initialize Stadsd Mock Client."""
        self.logger = logging.getLogger()
        self.logger.warning("statsd failed to initialize")

    def incr(self, message: str):
        """Incrament a counter - mocked."""
        self.logger.debug(f"statsd not initialized - incr call: {message}")

    def decr(self, message: str):
        """Decrament a counter - mocked."""
        self.logger.debug(f"statsd not initialized - decr call: {message}")

    def timer(self, message: str):
        """Record timer information - mocked."""
        self.logger.debug(f"statsd not initialized - timer call: {message}")

        class Timer:
            def start(self):
                pass

            def stop(self):
                pass

        return Timer()
