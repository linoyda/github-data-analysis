import logging

def setup_logging(log_to_file: bool, debug_mode: bool):
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logger = logging.getLogger()
    logger.setLevel(log_level)
    handler = logging.FileHandler('analysis_output.log') if log_to_file else logging.StreamHandler()
    handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)