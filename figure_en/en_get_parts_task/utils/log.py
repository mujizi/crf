import logging


class Log():
    def __init__(self, path):
        logging.basicConfig(level=logging.INFO,
                            filename=path,
                            filemode='w')