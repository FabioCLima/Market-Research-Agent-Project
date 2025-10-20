try:
    from loguru import logger  # type: ignore
except Exception:
    import logging

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    logger = logging.getLogger("udaplay")

    # Provide compatible methods used in the code
    class _LoggerWrapper:
        def __init__(self, lg):
            self._lg = lg

        def info(self, *args, **kwargs):
            self._lg.info(" ".join(str(a) for a in args))

        def debug(self, *args, **kwargs):
            self._lg.debug(" ".join(str(a) for a in args))

        def warning(self, *args, **kwargs):
            self._lg.warning(" ".join(str(a) for a in args))

        def error(self, *args, **kwargs):
            self._lg.error(" ".join(str(a) for a in args))

    logger = _LoggerWrapper(logger)
