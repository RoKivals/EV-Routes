import logging

def setup_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Если логгер уже имеет обработчики, не добавляем их снова
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()