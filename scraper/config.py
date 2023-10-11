import logging

def setup_logging():
    logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG)
