import logging

class _Logger:
    __instance = None
    def __init__(self):
        if _Logger.__instance:
            return

        self._logging = logging
        self._format = "[%(levelname)s] [%(asctime)s] %(message)s"
        self._logging.basicConfig(
            format=self._format,
            level=logging.INFO
        )

        self._logger = self._logging.getLogger(__name__)
        self._default_log_method = self.info

        _Logger._instance = self

    def info(self, message: str):
        self._logger.info(f"{message}")
        
    def debug(self, message: str):
        self._logger.debug(f"{message}")

    def warning(self, message: str):
        self._logger.warning(f"{message}")

    def error(self, message: str):
        self._logger.error(f"{message}")

    def log(self, message: str):
        self._default_log_method(message)

Logger = _Logger()
