#!/usr/bin/env python
"""
 Created by Dai at 18-10-31.
"""

import logging


def get_logger(name='widow'):
    logging_format = "[%(process)d][%(asctime)s]-%(name)s-%(levelname)-6s"
    # logging_format += "%(module)-7s::l%(lineno)d: "
    logging_format += "%(module)-7s: "
    logging_format += "%(message)s"

    logging.basicConfig(
        format=logging_format,
        level=logging.DEBUG
    )
    logging.getLogger("asyncio").setLevel(logging.INFO)

    return logging.getLogger(name)
