from functools import reduce
import logging


prefix = "MLPC: "


def error(*msg):
    logging.error(_as_single_msg_with_prefix(*msg))


def warning(*msg):
    logging.warning(_as_single_msg_with_prefix(*msg))


def info(*msg):
    logging.info(_as_single_msg_with_prefix(*msg))


def debug(*msg):
    logging.debug(_as_single_msg_with_prefix(*msg))


def _as_single_msg_with_prefix(*msg):
    if len(msg) > 1:
        as_strings = map(lambda x: str(x), msg)
        single_string = reduce(lambda s1, s2: s1 + " " + s2, as_strings)
        return prefix + single_string
    else:
        return prefix + msg[0]
