import logging

try:
    import colorlog

    formatter = colorlog.ColoredFormatter(log_colors=colorlog.default_log_colors)
    handler = colorlog.StreamHandler()
    handler.setFormatter(formatter)
except ImportError:
    handler = logging.StreamHandler()
    print("Install colorlog!")


logger = logging.getLogger("caeroc-app")
logger.addHandler(handler)
logger.setLevel("DEBUG")
logger.info("caeroc: Compressible Aerodynamics Calculator")
