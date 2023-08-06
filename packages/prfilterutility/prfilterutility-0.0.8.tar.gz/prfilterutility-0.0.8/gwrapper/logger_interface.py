import logging


class ExampleLogger(object):
    @staticmethod
    def log(*params):
        pass


class ChildLogger(ExampleLogger):
    def __init__(
        self,
        handler=logging.StreamHandler(),
        logger_name=__name__,
        min_level=logging.INFO
    ):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(min_level)
        self.logger.handlers = [handler]

    def log(self, log_level, message):
        self.logger.log(log_level, message)


class NoOpLogger(ExampleLogger):
    def __init__(
        self,
        handler=logging.StreamHandler(),
        logger_name=__name__,
        min_level=logging.INFO
    ):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(min_level)
        self.logger.handlers = [handler]
