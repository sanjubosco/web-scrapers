import logging
from nccprops import fileloc

""" Logging functionality for the project """
## logging for ml training
formatlogger = logging.getLogger('formatlogger')
format_formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(module)s:%(funcName)s:%(lineno)d:%(message)s')
formatlogger.setLevel(logging.DEBUG)
## this is for logging to file
format_file_handler = logging.FileHandler(fileloc.LOG_FORMAT)
format_file_handler.setFormatter(format_formatter)

## this is for console logging
format_stream_handler = logging.StreamHandler()
format_stream_handler.setFormatter(format_formatter)
format_stream_handler.setLevel(logging.INFO)

formatlogger.addHandler(format_file_handler)
formatlogger.addHandler(format_stream_handler)


